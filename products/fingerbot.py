"""Test case product config — ADAPROX Fingerbot smart switch-pusher.

All 4 beat prompts are drafted. Beat 2 comes verbatim from the handoff
brief; beats 1, 3, and 4 were written to match its established look (same
bedroom, same white light switch, same left-side window light, same
light-medium skin tone) so the 4 images hold together as one consistent set
per the cross-cutting requirements in image-generation-animation-requirements.md.
"""

BEAT1_PROMPT = (
    "A candid UGC-style vertical photo capturing a relatable everyday "
    "moment: a hand and forearm reaching out from under a bedsheet at "
    "night, straining toward a traditional white wall-mounted light switch "
    "across the room, visibly too far to reach comfortably — capturing the "
    '"too tired to get up and turn off the light" feeling. The switch and '
    "a sliver of the bedroom wall sit in the lower-center of the frame, "
    "softly lit; the upper two-thirds of the vertical frame is left open "
    "and uncluttered for a hook text overlay. Same bedroom as the rest of "
    "this set: a plain wall with a plain white switch plate, softly "
    "blurred where out of focus. Natural window lighting from the left "
    "casting soft, warm shadows, no harsh studio lighting. Skin tone: "
    "light-medium, matching hand. Phone-camera aesthetic, slightly grainy "
    "and candid, not polished. No face visible."
)

BEAT1_NEGATIVE_PROMPT = (
    "studio lighting, white seamless background, multiple hands, blurry "
    "hand, text, watermark, logo overlay, harsh shadows, low resolution, "
    "staged or posed look"
)

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

BEAT3_PROMPT = (
    "A close-up UGC-style vertical photo, tighter framing than a standard "
    "product shot, showing the white Fingerbot device mounted directly on "
    "top of a wall light switch, its small mechanical arm extended "
    "downward mid-press, physically pushing the switch toggle at the exact "
    "moment of activation. A sliver of the same softly blurred bedroom "
    "wall is visible around the switch. In the background, subtly out of "
    "focus, a bedside lamp is visibly lit, making the cause-and-effect "
    "obvious even as a still frame. Natural window lighting from the "
    "left, same direction and softness as the rest of this set, soft "
    "shadows, no harsh studio lighting. Product and switch in sharp "
    "focus, mechanical arm clearly mid-motion. Shot vertically, "
    "phone-camera aesthetic, slightly candid angle. No hand or face in "
    "frame — device caught mid-action on its own."
)

BEAT3_NEGATIVE_PROMPT = (
    "studio lighting, white seamless background, hand in frame, blurry "
    "action, motion blur obscuring the arm, text, watermark, logo overlay, "
    "dark shadows, low resolution, static or idle-looking device"
)

BEAT4_PROMPT = (
    "A bright, clean, well-exposed vertical product photo of the Fingerbot "
    'device sitting next to its retail packaging box (small white box with '
    '"ADAPROX Fingerbot" branding clearly legible) on a nightstand in the '
    "same bedroom setting as the rest of this set. Device and box both in "
    "sharp focus, product occupying the upper two-thirds of frame, "
    "centered. The bottom third of the vertical frame is left clear, "
    "evenly lit and uncluttered, reserved for bold price/offer text "
    "overlay. Lighting is bright and even — natural window light from the "
    "left, same direction as the rest of the set, but brighter and more "
    "evenly diffused than the earlier candid shots, giving a more "
    'polished "product shot" credibility to this final frame. No dark '
    "corners, no shadows obscuring the product or box. Shot vertically, "
    "phone-camera aesthetic but cleaner and more deliberate than the hook "
    "shot. No hand or face needed in this shot — product and packaging "
    "only."
)

BEAT4_NEGATIVE_PROMPT = (
    "dark lighting, dim shadows, blurry product, blurry packaging, "
    "cluttered background, text baked into image, watermark, low "
    "resolution, busy background"
)

PRODUCT_CONFIG = {
    "name": "fingerbot",
    "output_dir": "output/fingerbot",
    "product_asset_path": None,
    "beats": {
        "1": {
            "prompt": BEAT1_PROMPT,
            "negative_prompt": BEAT1_NEGATIVE_PROMPT,
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
            "prompt": BEAT3_PROMPT,
            "negative_prompt": BEAT3_NEGATIVE_PROMPT,
            "kling_prompt": (
                "The mechanical arm presses down firmly on the switch, "
                "completing the press, light state visibly changes at the "
                "moment of contact"
            ),
            "kling_negative_prompt": (
                "fast zoom, spin, camera shake, motion blur, jump cut"
            ),
            "camera_params": {},
            "trim_start": 0,
            "trim_duration": 2.8,
        },
        "4": {
            "prompt": BEAT4_PROMPT,
            "negative_prompt": BEAT4_NEGATIVE_PROMPT,
            "duration": 1.8,
            "zoom_direction": "in",
        },
    },
}
