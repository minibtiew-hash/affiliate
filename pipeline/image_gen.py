import base64
import os

from google import genai

from pipeline import config, cost_tracker


def generate_image(
    prompt: str,
    negative_prompt: str = "",
    reference_images: list[str] | None = None,
    aspect_ratio: str = "9:16",
    output_path: str = "output.png",
) -> str:
    """Generate one image via Nano Banana 2 (Gemini image model).

    reference_images: local file paths of prior images (e.g. beat 1) to pass
    as reference input for consistency, per the multi-image compositing spec.
    """
    config.require_gemini_key()
    client = genai.Client()

    full_prompt = prompt
    if negative_prompt:
        full_prompt += f"\n\nAvoid: {negative_prompt}"

    input_content = [{"type": "text", "text": full_prompt}]
    for ref_path in reference_images or []:
        with open(ref_path, "rb") as f:
            ref_bytes = f.read()
        input_content.append(
            {
                "type": "image",
                "data": base64.b64encode(ref_bytes).decode("utf-8"),
                "mime_type": "image/png",
            }
        )

    # generation_config.image_config.aspect_ratio is deprecated in this SDK
    # version — the live path is response_format={"type": "image", ...}.
    interaction = client.interactions.create(
        model=config.GEMINI_MODEL,
        input=input_content,
        response_format={
            "type": "image",
            "aspect_ratio": aspect_ratio,
            "image_size": "1K",
        },
    )

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(interaction.output_image.data))

    cost_tracker.log_image_call(model=config.GEMINI_MODEL)

    return output_path
