import json
import os
import subprocess
import tempfile

TARGET_SIZE = "1080x1920"
TARGET_FPS = 25

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# zone -> (y expression as fraction of frame height, font size)
TEXT_ZONES = {
    "upper_third": (0.12, 64),
    "center": (0.45, 64),
    "lower_third_light": (0.78, 48),
    "lower_third_bold": (0.82, 64),
}


def get_duration(path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def trim_clip(input_path: str, start: float, duration: float, output_path: str) -> str:
    # Input-side seek (-ss before -i) + re-encode, not "-c copy" — stream
    # copy on Kling's encoded output produced empty files ("Output file is
    # empty, nothing was encoded"), confirmed live 2026-07-10. Re-encoding
    # is slightly slower but reliable regardless of source keyframe layout.
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(start),
            "-i",
            input_path,
            "-t",
            str(duration),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            output_path,
        ],
        check=True,
        capture_output=True,
    )
    return output_path


def zoom_pan_clip(
    image_path: str,
    duration: float,
    output_path: str,
    zoom_direction: str = "in",
    fps: int = 25,
    size: str = "1080x1920",
) -> str:
    frames = int(duration * fps)
    if zoom_direction == "in":
        zoom_expr = "min(zoom+0.0015,1.2)"
    elif zoom_direction == "out":
        zoom_expr = "max(zoom-0.0015,1.0)"
    else:
        raise ValueError(f"zoom_direction must be 'in' or 'out', got {zoom_direction!r}")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            image_path,
            "-vf",
            f"zoompan=z='{zoom_expr}':d={frames}:s={size}",
            "-t",
            str(duration),
            "-r",
            str(fps),
            output_path,
        ],
        check=True,
        capture_output=True,
    )
    return output_path


def normalize_clip(
    input_path: str, output_path: str, size: str = TARGET_SIZE, fps: int = TARGET_FPS
) -> str:
    """Re-encode to a common resolution/fps/pixel format so clips from
    different sources (Kling vs zoompan) can be stream-copied together in
    stitch_clips. Without this, mismatched resolutions (e.g. Kling's
    716x1280-ish raw output vs zoompan's 1080x1920) break concat.
    """
    width, height = size.split("x")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},fps={fps}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            output_path,
        ],
        check=True,
        capture_output=True,
    )
    return output_path


def add_text_overlay(
    input_path: str, text: str, zone: str, output_path: str, font_color: str = "white"
) -> str:
    """Burn in a single line of static text at a fixed screen zone.

    zone: one of TEXT_ZONES ("upper_third", "center", "lower_third_light",
    "lower_third_bold").
    """
    if zone not in TEXT_ZONES:
        raise ValueError(f"zone must be one of {list(TEXT_ZONES)}, got {zone!r}")
    y_frac, font_size = TEXT_ZONES[zone]

    escaped_text = text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")

    drawtext = (
        f"drawtext=fontfile={FONT_PATH}:text='{escaped_text}':"
        f"fontsize={font_size}:fontcolor={font_color}:"
        f"borderw=3:bordercolor=black:"
        f"x=(w-text_w)/2:y=h*{y_frac}"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            drawtext,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            output_path,
        ],
        check=True,
        capture_output=True,
    )
    return output_path


def stitch_clips(clip_paths: list[str], output_path: str, max_duration: float = 10.0) -> str:
    normalized_paths = []
    for i, path in enumerate(clip_paths):
        norm_path = os.path.join(
            os.path.dirname(output_path) or ".", f"_normalized_{i}.mp4"
        )
        normalize_clip(path, norm_path)
        normalized_paths.append(norm_path)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as concat_file:
        for path in normalized_paths:
            concat_file.write(f"file '{os.path.abspath(path)}'\n")
        concat_list_path = concat_file.name

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                concat_list_path,
                "-c",
                "copy",
                output_path,
            ],
            check=True,
            capture_output=True,
        )
    finally:
        os.remove(concat_list_path)
        for path in normalized_paths:
            os.remove(path)

    duration = get_duration(output_path)
    if duration >= max_duration:
        raise ValueError(
            f"Stitched video is {duration:.2f}s, exceeds the {max_duration}s hard limit"
        )

    return output_path
