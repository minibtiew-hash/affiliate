import json
import os
import subprocess
import tempfile
import textwrap

TARGET_SIZE = "1080x1920"
TARGET_FPS = 25

# Poppins ExtraBold (OFL) — the standard social-caption look. The earlier
# DejaVu Sans default read as "AI-generated" per user feedback 2026-07-13.
FONT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "fonts", "Poppins-ExtraBold.ttf",
)

# zone -> (y as fraction of frame height, font size). Values keep text inside
# the 9:16 MOBILE-SAFE area: platform UI (Shopee/TikTok) covers roughly the
# top ~8%, the bottom ~22% (captions/buttons/progress bar), and the right
# ~15% (action buttons) — text must never sit in those bands.
TEXT_ZONES = {
    "upper_third": (0.16, 60),
    "center": (0.42, 60),
    "lower_third_light": (0.64, 46),
    "lower_third_bold": (0.68, 60),
}

# Max text width as a fraction of frame width before wrapping onto a new
# line — keeps text clear of the right-side action buttons and screen edges.
TEXT_SAFE_WIDTH_FRAC = 0.80
# Rough average glyph width for Poppins ExtraBold, as a fraction of fontsize.
_AVG_CHAR_WIDTH_EM = 0.60


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


def _wrap_for_width(text: str, font_size: int, frame_width: int) -> str:
    """Wrap text so no line exceeds the mobile-safe width — ffmpeg's drawtext
    does NOT wrap on its own, so an unwrapped long line silently runs off
    both frame edges (this happened live: the beat 1 hook line was ~1600px
    wide on a 1080px frame).
    """
    max_line_px = frame_width * TEXT_SAFE_WIDTH_FRAC
    chars_per_line = max(8, int(max_line_px / (font_size * _AVG_CHAR_WIDTH_EM)))
    return "\n".join(textwrap.wrap(text, width=chars_per_line))


def add_text_overlay(
    input_path: str, text: str, zone: str, output_path: str, font_color: str = "white"
) -> str:
    """Burn in static caption text at a fixed mobile-safe screen zone,
    auto-wrapping onto multiple lines to stay inside the safe width.

    zone: one of TEXT_ZONES ("upper_third", "center", "lower_third_light",
    "lower_third_bold").
    """
    if zone not in TEXT_ZONES:
        raise ValueError(f"zone must be one of {list(TEXT_ZONES)}, got {zone!r}")
    y_frac, font_size = TEXT_ZONES[zone]

    frame_width = int(TARGET_SIZE.split("x")[0])
    wrapped = _wrap_for_width(text, font_size, frame_width)

    # textfile= instead of text= — inline filter escaping silently ate
    # apostrophes ("Don't" rendered as "Dont", caught live 2026-07-14).
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as text_file:
        text_file.write(wrapped)
        text_file_path = text_file.name

    drawtext = (
        f"drawtext=fontfile={FONT_PATH}:textfile={text_file_path}:"
        f"fontsize={font_size}:fontcolor={font_color}:"
        f"borderw=4:bordercolor=black@0.9:"
        f"line_spacing=12:"
        f"x=(w-text_w)/2:y=h*{y_frac}"
    )

    try:
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
    finally:
        os.remove(text_file_path)
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
