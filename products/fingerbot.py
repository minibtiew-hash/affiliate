"""Test case product config — ADAPROX Fingerbot smart switch-pusher.

Only beat 2's prompt is finalized (drafted in the handoff brief). Beats 1, 3,
and 4 are TODO per MASTER-TODO.md immediate next step #4 — draft them next,
using beat 1's output as a reference image for beats 2-4 once all four are
written.
"""

BEAT2_PROMPT = (
    'A close-up UGC-style photo of a hand holding a small white smart home '
    'device called a "Fingerbot" — a compact rectangular white plastic '
    "gadget roughly the size of a matchbox, with a small mechanical arm on "
    "one side. The hand holds it at chest height, fingers wrapping naturally "
    "around the sides, thumb visible, product tilted slightly toward camera "
    "so its full shape and the mechanical arm are clearly visible. "
    "Background is a softly blurred bedroom wall with a white light switch "
    "faintly visible out of focus. Natural window lighting from the left, "
    "soft shadows, no harsh studio lighting. Product is in sharp focus, "
    "occupying roughly 40% of the vertical frame, positioned center-right. "
    "Shot vertically, phone-camera aesthetic, slightly candid angle — not a "
    "polished studio product shot. Skin tone: light-medium. No visible face, "
    "hand only."
)

BEAT2_NEGATIVE_PROMPT = (
    "studio lighting, white seamless background, multiple hands, blurry "
    "product, motion blur, text, watermark, logo overlay, dark shadows, low "
    "resolution"
)

PRODUCT_CONFIG = {
    "name": "fingerbot",
    "output_dir": "output/fingerbot",
    "product_asset_path": None,
    "beats": {
        "1": {
            "prompt": None,  # TODO: draft hook-shot prompt
            "negative_prompt": None,
            "duration": 1.8,
            "zoom_direction": "in",
        },
        "2": {
            "prompt": BEAT2_PROMPT,
            "negative_prompt": BEAT2_NEGATIVE_PROMPT,
            "kling_prompt": (
                "Hand slowly rotates the device toward camera, revealing its "
                "full shape"
            ),
            "kling_negative_prompt": "fast zoom, spin, motion blur, shaky camera",
            "camera_params": {},
            "trim_start": 0,
            "trim_duration": 2.3,
        },
        "3": {
            "prompt": None,  # TODO: draft proof/demo prompt
            "negative_prompt": None,
            "kling_prompt": None,
            "kling_negative_prompt": None,
            "camera_params": {},
            "trim_start": 0,
            "trim_duration": 2.8,
        },
        "4": {
            "prompt": None,  # TODO: draft CTA close prompt
            "negative_prompt": None,
            "duration": 1.8,
            "zoom_direction": "in",
        },
    },
}
