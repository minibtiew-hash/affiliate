import os

from pipeline import ffmpeg_utils, image_gen, storage, video_gen


def generate_video_from_product(product_config: dict) -> str:
    """Run the full 4-beat pipeline for one product and return the final video path.

    product_config shape:
    {
        "name": str,
        "output_dir": str,
        "product_asset_path": str | None,  # extra reference image for beats 2-4
        "beats": {
            "1": {"prompt", "negative_prompt", "duration", "zoom_direction"},
            "2": {"prompt", "negative_prompt", "kling_prompt", "kling_negative_prompt",
                  "camera_params", "trim_start", "trim_duration"},
            "3": {same shape as beat 2},
            "4": {"prompt", "negative_prompt", "duration", "zoom_direction"},
        },
    }
    """
    out_dir = product_config["output_dir"]
    os.makedirs(out_dir, exist_ok=True)
    beats = product_config["beats"]
    product_asset = product_config.get("product_asset_path")

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

    # Beats 1 & 4: local Ken Burns zoom/pan, no Kling call.
    clip1 = ffmpeg_utils.zoom_pan_clip(
        image_path=beat1_image,
        duration=beats["1"]["duration"],
        zoom_direction=beats["1"].get("zoom_direction", "in"),
        output_path=os.path.join(out_dir, "clip1.mp4"),
    )
    clip4 = ffmpeg_utils.zoom_pan_clip(
        image_path=beat4_image,
        duration=beats["4"]["duration"],
        zoom_direction=beats["4"].get("zoom_direction", "in"),
        output_path=os.path.join(out_dir, "clip4.mp4"),
    )

    # Kling needs a reachable URL, not a local path — upload beat 2 & 3 first.
    beat2_url = storage.upload_file(beat2_image, dest_blob_name=f"{product_config['name']}/beat2.png")
    beat3_url = storage.upload_file(beat3_image, dest_blob_name=f"{product_config['name']}/beat3.png")

    # Beats 2 & 3: Kling image2video at 5s, then trim to the beat's target duration.
    beat2_raw_url = video_gen.generate_video(
        image_path_or_url=beat2_url,
        prompt=beats["2"]["kling_prompt"],
        negative_prompt=beats["2"].get("kling_negative_prompt", ""),
        camera_params=beats["2"].get("camera_params"),
    )
    beat3_raw_url = video_gen.generate_video(
        image_path_or_url=beat3_url,
        prompt=beats["3"]["kling_prompt"],
        negative_prompt=beats["3"].get("kling_negative_prompt", ""),
        camera_params=beats["3"].get("camera_params"),
    )

    # generate_video returns a remote URL — download locally before trimming.
    beat2_raw_local = storage.download_file(
        beat2_raw_url, os.path.join(out_dir, "beat2_raw_5s.mp4")
    )
    beat3_raw_local = storage.download_file(
        beat3_raw_url, os.path.join(out_dir, "beat3_raw_5s.mp4")
    )

    clip2 = ffmpeg_utils.trim_clip(
        input_path=beat2_raw_local,
        start=beats["2"].get("trim_start", 0),
        duration=beats["2"]["trim_duration"],
        output_path=os.path.join(out_dir, "clip2.mp4"),
    )
    clip3 = ffmpeg_utils.trim_clip(
        input_path=beat3_raw_local,
        start=beats["3"].get("trim_start", 0),
        duration=beats["3"]["trim_duration"],
        output_path=os.path.join(out_dir, "clip3.mp4"),
    )

    final_path = os.path.join(out_dir, "final.mp4")
    return ffmpeg_utils.stitch_clips([clip1, clip2, clip3, clip4], final_path)
