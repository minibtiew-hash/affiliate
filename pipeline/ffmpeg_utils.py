import json
import os
import subprocess
import tempfile


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
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-ss",
            str(start),
            "-t",
            str(duration),
            "-c",
            "copy",
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


def stitch_clips(clip_paths: list[str], output_path: str, max_duration: float = 10.0) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as concat_file:
        for path in clip_paths:
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

    duration = get_duration(output_path)
    if duration >= max_duration:
        raise ValueError(
            f"Stitched video is {duration:.2f}s, exceeds the {max_duration}s hard limit"
        )

    return output_path
