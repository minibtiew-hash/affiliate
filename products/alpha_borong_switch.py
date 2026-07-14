"""Product config — Alpha Borong Wireless Remote-Control Switch / Smart
Light Controller (real Shopee listing, confirmed via screenshot 2026-07-09
after the original "ADAPROX Fingerbot" name from the handoff brief turned
out to be a placeholder, not the actual product).

Real product facts (from listing screenshot): white switch-cover panel with
a mechanical arm that physically presses an existing wall light switch, a
separate wireless receiver cube (USB-powered), and a handheld ON/OFF remote
control. Selling points: long battery life, wireless convenience, no need
to drill holes.

All 4 beat prompts are drafted. Beats 1-3 keep the mechanical-arm visual
concept from the original draft (still accurate to the real product) but
beat 4's packaging text has been corrected from the placeholder brand to
Alpha Borong, and now includes the remote control since that's a real
differentiator for this listing. Same bedroom, same white light switch,
same left-side warm lamp light, same light-medium skin tone across all 4
for consistency per image-generation-animation-requirements.md.

Lighting note (fixed 2026-07-09): the scenario is nighttime — too tired to
get up and turn off the light — so beats 1-3 are lit by a warm bedside lamp
glow, not daylight/window light. An earlier draft said "night" but also
said "natural window lighting," which contradicted itself and produced
bright morning-looking renders. Beat 4 is intentionally brighter per the
CTA spec (never end dark), narratively justified as the lamp now being
fully switched on.
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
    "blurred where out of focus. It is genuinely nighttime — the room is "
    "dim and dark, lit only by a warm, soft lamp glow coming from the left "
    "side of frame (a bedside lamp just out of shot), casting warm shadows. "
    "No daylight, no window light, no sunlight anywhere in the shot. Skin "
    "tone: light-medium, matching hand. Phone-camera aesthetic, slightly "
    "grainy and candid, not polished. No face visible."
)

BEAT1_NEGATIVE_PROMPT = (
    "studio lighting, white seamless background, multiple hands, blurry "
    "hand, text, watermark, logo overlay, harsh shadows, low resolution, "
    "staged or posed look, daylight, sunlight, bright window light, "
    "morning light, daytime"
)

BEAT2_PROMPT = (
    "A close-up UGC-style photo of a hand holding a small white wireless "
    "smart switch-pusher device — a compact rectangular white plastic "
    "gadget roughly the size of a matchbox, with a small mechanical arm on "
    "one side. The hand holds it at chest height, fingers wrapping naturally "
    "around the sides, thumb visible, product tilted slightly toward camera "
    "so its full shape and the mechanical arm are clearly visible. "
    "Background is a softly blurred bedroom wall with a white light switch "
    "faintly visible out of focus. It is nighttime, same dim room as the "
    "rest of this set, lit only by a warm lamp glow from the left (same "
    "bedside lamp) — no daylight or window light — but the product itself "
    "is clearly and evenly lit despite the dim ambient room, soft warm "
    "shadows, no harsh studio lighting. Product is in sharp focus, "
    "occupying roughly 40% of the vertical frame, positioned center-right. "
    "Shot vertically, phone-camera aesthetic, slightly candid angle — not a "
    "polished studio product shot. Skin tone: light-medium. No visible face, "
    "hand only."
)

BEAT2_NEGATIVE_PROMPT = (
    "studio lighting, white seamless background, multiple hands, blurry "
    "product, motion blur, text, watermark, logo overlay, dark shadows, low "
    "resolution, daylight, sunlight, bright window light, morning light, "
    "daytime"
)

# Beat 3 rewritten 2026-07-10 after the first end-to-end video: the original
# "device pressing the switch on its own, light changing state" demo read as
# unrealistic/CGI. Root causes and the universal fixes now documented in
# image-generation-animation-requirements.md ("Demo beat realism principles"):
# show the human trigger in-frame, never ask the video model for a scene
# state change, and explicitly anchor what stays still.
BEAT3_PROMPT = (
    "A UGC-style vertical photo shot like a phone propped on a nightstand: "
    "in the near foreground, slightly low in frame, a hand holds the small "
    "gray remote control with the thumb resting on its ON/OFF button, "
    "remote angled toward the wall. In the mid-ground, in sharp focus, the "
    "white wireless switch-pusher device is mounted on top of the wall "
    "light switch, its small mechanical arm resting just above the switch "
    "toggle, poised to press. Both the remote in the hand and the device "
    "on the switch are clearly visible in the same frame, so the "
    "cause-and-effect relationship is obvious at a glance. The bedside "
    "lamp is already on, giving the same warm glow from the left as the "
    "rest of this set — it is nighttime, dim room, no daylight or window "
    "light anywhere, soft warm shadows, no harsh studio lighting. Same "
    "hand, same skin tone (light-medium), same bedroom and white switch "
    "plate as the other shots in this set. Phone-camera aesthetic, candid "
    "framing, very slightly imperfect angle. No face visible."
)

BEAT3_NEGATIVE_PROMPT = (
    "studio lighting, white seamless background, multiple hands, extra "
    "fingers, blurry product, text, watermark, logo overlay, dark shadows, "
    "low resolution, daylight, sunlight, bright window light, morning "
    "light, daytime, floating device, device detached from wall"
)

BEAT4_PROMPT = (
    "A bright, clean, well-exposed vertical product photo of the white "
    "wireless switch-pusher device sitting next to its small handheld "
    "remote control (a simple gray remote with ON and OFF buttons) and its "
    'retail packaging box (small white box with "Alpha Borong" branding '
    "clearly legible) on a nightstand in the same bedroom setting as the "
    "rest of this set. Device, remote, and box all in sharp focus, "
    "arranged neatly, product occupying the upper two-thirds of frame, "
    "centered. The bottom third of the vertical frame is left clear, "
    "evenly lit and uncluttered, reserved for bold price/offer text "
    "overlay. Still nighttime, same bedroom as the rest of the set, but the "
    "bedside lamp from the earlier shots is now fully switched on and "
    "positioned to the left, brightly and evenly illuminating the whole "
    "scene — no daylight or window light, just the lamp now at full "
    "brightness, warmer and more evenly diffused than the dim earlier "
    'shots, giving a more polished "product shot" credibility to this '
    "final frame. No dark corners, no shadows obscuring the product, "
    "remote, or box. Shot "
    "vertically, phone-camera aesthetic but cleaner and more deliberate "
    "than the hook shot. No hand or face needed in this shot — product, "
    "remote, and packaging only."
)

BEAT4_NEGATIVE_PROMPT = (
    "dark lighting, dim shadows, blurry product, blurry packaging, "
    "cluttered background, text baked into image, watermark, low "
    "resolution, busy background"
)

    # 2026-07-09 restructure (user decision): total video target ~8s, not the
    # full 10s allowed — beat 1 now gets real Kling animation (hand straining
    # to reach the switch reads better animated than static), beat 2 drops to
    # local zoom/pan only (reveal doesn't need motion at 1s). Beat 3 stays
    # Kling, beat 4 stays local. Still 2 Kling calls per video, just swapped.
    # overlay_text values are DRAFTS reflecting the user's direction, not
    # approved final ad copy — confirm exact wording before shipping.

PRODUCT_CONFIG = {
    "name": "alpha_borong_switch",
    "output_dir": "output/alpha_borong_switch",
    "product_asset_path": None,
    "beats": {
        "1": {
            "prompt": BEAT1_PROMPT,
            "negative_prompt": BEAT1_NEGATIVE_PROMPT,
            "kling_prompt": (
                "The hand and arm slowly stretch further out from under the "
                "blanket, straining toward the switch, natural subtle "
                "handheld phone-camera drift"
            ),
            "kling_negative_prompt": (
                "fast zoom, spin, camera shake, motion blur, jump cut"
            ),
            "camera_params": {},
            "trim_start": 0,
            "trim_duration": 3.0,
            "overlay_text": "POV: too lazy to get up and turn off the light",
            "overlay_zone": "upper_third",
            # std mode while still validating quality/cost - switch to "pro"
            # (or remove this key, pro is the default) once ready for final.
            "kling_mode": "std",
        },
        "2": {
            "prompt": BEAT2_PROMPT,
            "negative_prompt": BEAT2_NEGATIVE_PROMPT,
            "duration": 1.0,
            "zoom_direction": "in",
            # "Now introducing..." framing per user 2026-07-13 — signals to
            # the viewer that THIS is the product being sold, not just a scene.
            "overlay_text": "Now introducing: the wireless switch clicker",
            "overlay_zone": "lower_third_light",
        },
        "3": {
            "prompt": BEAT3_PROMPT,
            "negative_prompt": BEAT3_NEGATIVE_PROMPT,
            "kling_prompt": (
                "The thumb presses the remote button once with a small, "
                "natural click motion, and a moment later the small "
                "mechanical arm on the wall device pushes down on the light "
                "switch with one short, firm, mechanical movement. Nothing "
                "else in the scene moves: the camera stays completely "
                "static, the lamp stays on, the lighting does not change, "
                "the hand stays in place apart from the thumb press."
            ),
            "kling_negative_prompt": (
                "camera movement, zoom, pan, spin, camera shake, motion "
                "blur, jump cut, lighting change, light flicker, morphing, "
                "warping, object deformation, extra fingers, hand distortion"
            ),
            "camera_params": {},
            "trim_start": 0,
            "trim_duration": 3.0,
            "overlay_text": "Just tap once",
            "overlay_zone": "upper_third",
            "kling_mode": "std",
        },
        "4": {
            "prompt": BEAT4_PROMPT,
            "negative_prompt": BEAT4_NEGATIVE_PROMPT,
            "duration": 1.0,
            "zoom_direction": "in",
            "overlay_text": "Don't need to stand up again",
            "overlay_zone": "lower_third_bold",
        },
    },
}
