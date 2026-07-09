"""Standalone test: animate the Fingerbot beat 2 image via Kling.

Per MASTER-TODO.md immediate next step #6 — run only after
test_generate_image.py has produced output/fingerbot/beat2_test.png.
Requires KLING_API_KEY in .env, and an image URL Kling can fetch (upload the
local PNG to a CDN/bucket first — Kling's `image` field needs a reachable
URL or base64, not a local path).
"""
from products.fingerbot import PRODUCT_CONFIG

from pipeline.video_gen import generate_video

if __name__ == "__main__":
    beat2 = PRODUCT_CONFIG["beats"]["2"]
    image_url = "REPLACE_WITH_UPLOADED_BEAT2_IMAGE_URL"

    clip_url = generate_video(
        image_path_or_url=image_url,
        prompt=beat2["kling_prompt"],
        negative_prompt=beat2["kling_negative_prompt"],
        camera_params=beat2["camera_params"],
    )
    print(f"Raw 5s clip URL: {clip_url}")
