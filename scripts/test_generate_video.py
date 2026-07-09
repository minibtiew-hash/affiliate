"""Standalone test: animate the Alpha Borong beat 2 image via Kling.

Run only after test_generate_image.py / test_generate_remaining_beats.py
have produced output/alpha_borong_switch/beat2.png. Requires KLING_API_KEY
and GCS credentials (GCS_BUCKET_NAME, GOOGLE_APPLICATION_CREDENTIALS) in
.env — the local PNG is uploaded to GCS first since Kling needs a reachable
URL, not a local path.
"""
from products.alpha_borong_switch import PRODUCT_CONFIG

from pipeline import storage
from pipeline.video_gen import generate_video

if __name__ == "__main__":
    beat2 = PRODUCT_CONFIG["beats"]["2"]
    local_image = f"{PRODUCT_CONFIG['output_dir']}/beat2.png"

    image_url = storage.upload_file(
        local_image, dest_blob_name=f"{PRODUCT_CONFIG['name']}/beat2.png"
    )
    print(f"Uploaded to: {image_url}")

    clip_url = generate_video(
        image_path_or_url=image_url,
        prompt=beat2["kling_prompt"],
        negative_prompt=beat2["kling_negative_prompt"],
        camera_params=beat2["camera_params"],
    )
    print(f"Raw 5s clip URL: {clip_url}")
