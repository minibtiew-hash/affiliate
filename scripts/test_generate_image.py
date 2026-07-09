"""Standalone test: generate the Fingerbot beat 2 image via Nano Banana 2.

Per MASTER-TODO.md immediate next step #5 — validate one beat before
building the rest. Requires GEMINI_API_KEY in .env.
"""
from pipeline.image_gen import generate_image
from products.fingerbot import BEAT2_NEGATIVE_PROMPT, BEAT2_PROMPT

if __name__ == "__main__":
    path = generate_image(
        prompt=BEAT2_PROMPT,
        negative_prompt=BEAT2_NEGATIVE_PROMPT,
        aspect_ratio="9:16",
        output_path="output/fingerbot/beat2_test.png",
    )
    print(f"Saved: {path}")
