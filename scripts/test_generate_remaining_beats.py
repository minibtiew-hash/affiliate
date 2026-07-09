"""Generate beats 1, 3, 4 for Alpha Borong, referencing the already-approved
beat 2 image (and each other, as they're produced) for cross-beat
consistency. Run after test_generate_image.py has produced beat 2.
"""
from pipeline.image_gen import generate_image
from products.alpha_borong_switch import PRODUCT_CONFIG

OUT_DIR = PRODUCT_CONFIG["output_dir"]
BEAT2_PATH = f"{OUT_DIR}/beat2.png"

if __name__ == "__main__":
    beats = PRODUCT_CONFIG["beats"]

    beat1_path = generate_image(
        prompt=beats["1"]["prompt"],
        negative_prompt=beats["1"]["negative_prompt"],
        reference_images=[BEAT2_PATH],
        aspect_ratio="9:16",
        output_path=f"{OUT_DIR}/beat1.png",
    )
    print(f"Saved: {beat1_path}")

    beat3_path = generate_image(
        prompt=beats["3"]["prompt"],
        negative_prompt=beats["3"]["negative_prompt"],
        reference_images=[BEAT2_PATH, beat1_path],
        aspect_ratio="9:16",
        output_path=f"{OUT_DIR}/beat3.png",
    )
    print(f"Saved: {beat3_path}")

    beat4_path = generate_image(
        prompt=beats["4"]["prompt"],
        negative_prompt=beats["4"]["negative_prompt"],
        reference_images=[BEAT2_PATH, beat1_path, beat3_path],
        aspect_ratio="9:16",
        output_path=f"{OUT_DIR}/beat4.png",
    )
    print(f"Saved: {beat4_path}")
