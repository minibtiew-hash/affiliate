import os

from pipeline import ffmpeg_utils, image_gen, storage, video_gen


def _animate_beat(beat_num: str, beat_cfg: dict, image_path: str, out_dir: str, product_name: str) -> str:
    """Produce one beat's clip: Kling animation if kling_prompt is set,
    otherwise a local ffmpeg zoom/pan. Which beats get which treatment is
    data-driven per product, not hardcoded by beat number — the 2026-07-09
    restructure moved beat 1 onto Kling and beat 2 onto local zoom/pan,
    flipping the original assignment.
    """
    if "kling_prompt" in beat_cfg:
        image_url = storage.upload_file(
            image_path, dest_blob_name=f"{product_name}/beat{beat_num}.png"
        )
        raw_url = video_gen.generate_video(
            image_path_or_url=image_url,
            prompt=beat_cfg["kling_prompt"],
            negative_prompt=beat_cfg.get("kling_negative_prompt", ""),
            camera_params=beat_cfg.get("camera_params"),
        )
        raw_local = storage.download_file(
            raw_url, os.path.join(out_dir, f"beat{beat_num}_raw_5s.mp4")
        )
        clip = ffmpeg_utils.trim_clip(
            input_path=raw_local,
            start=beat_cfg.get("trim_start", 0),
            duration=beat_cfg["trim_duration"],
            output_path=os.path.join(out_dir, f"clip{beat_num}_raw.mp4"),
        )
    else:
        clip = ffmpeg_utils.zoom_pan_clip(
            image_path=image_path,
            duration=beat_cfg["duration"],
            zoom_direction=beat_cfg.get("zoom_direction", "in"),
            output_path=os.path.join(out_dir, f"clip{beat_num}_raw.mp4"),
        )

    if beat_cfg.get("overlay_text"):
        return ffmpeg_utils.add_text_overlay(
            input_path=clip,
            text=beat_cfg["overlay_text"],
            zone=beat_cfg.get("overlay_zone", "center"),
            output_path=os.path.join(out_dir, f"clip{beat_num}.mp4"),
        )
    return clip


def generate_video_from_product(product_config: dict) -> str:
    """Run the full 4-beat pipeline for one product and return the final video path.

    product_config shape:
    {
        "name": str,
        "output_dir": str,
        "product_asset_path": str | None,  # extra reference image for beats 2-4
        "beats": {
            "<1-4>": {
                "prompt", "negative_prompt",
                # Kling-animated beat:
                "kling_prompt", "kling_negative_prompt", "camera_params",
                "trim_start", "trim_duration",
                # OR local zoom/pan beat:
                "duration", "zoom_direction",
                # optional for either:
                "overlay_text", "overlay_zone",
            },
        },
    }
    """
    out_dir = product_config["output_dir"]
    os.makedirs(out_dir, exist_ok=True)
    beats = product_config["beats"]
    product_asset = product_config.get("product_asset_path")
    product_name = product_config["name"]

    # Beat 1: text-to-image, no references — this becomes the consistency anchor.
    beat1_image = image_gen.generate_image(
        prompt=beats["1"]["prompt"],
        negative_prompt=beats["1"].get("negative_prompt", ""),
        output_path=os.path.join(out_dir, "beat1.png"),
    )

    def refs_for_beat(extra: list[str] | None = None) -> list[str]:
        refs = [beat1_image]
        if product_asset:
            refs.append(product_asset)
        return refs + (extra or [])

    # Beats 2-4: image-to-image, referencing beat 1 (+ product asset) for consistency.
    beat2_image = image_gen.generate_image(
        prompt=beats["2"]["prompt"],
        negative_prompt=beats["2"].get("negative_prompt", ""),
        reference_images=refs_for_beat(),
        output_path=os.path.join(out_dir, "beat2.png"),
    )
    beat3_image = image_gen.generate_image(
        prompt=beats["3"]["prompt"],
        negative_prompt=beats["3"].get("negative_prompt", ""),
        reference_images=refs_for_beat([beat2_image]),
        output_path=os.path.join(out_dir, "beat3.png"),
    )
    beat4_image = image_gen.generate_image(
        prompt=beats["4"]["prompt"],
        negative_prompt=beats["4"].get("negative_prompt", ""),
        reference_images=refs_for_beat([beat2_image, beat3_image]),
        output_path=os.path.join(out_dir, "beat4.png"),
    )

    images = {"1": beat1_image, "2": beat2_image, "3": beat3_image, "4": beat4_image}
    clips = [
        _animate_beat(n, beats[n], images[n], out_dir, product_name)
        for n in ("1", "2", "3", "4")
    ]

    final_path = os.path.join(out_dir, "final.mp4")
    return ffmpeg_utils.stitch_clips(clips, final_path)
