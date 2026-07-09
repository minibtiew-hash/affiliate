# Image Generation + Animation Requirements
### Pipeline: 4 Photos → 4 Animated Clips → 1 Stitched Video (<10s)

This spec defines what to generate at the **image stage**, so that each image already carries everything it needs before animation.

---

## Pipeline Overview

```
[Image 1: Hook]  → animate → [Clip 1: ~1.5-2s]
[Image 2: Product Reveal] → animate → [Clip 2: ~2-2.5s]
[Image 3: Proof/Demo] → animate → [Clip 3: ~2.5-3s]
[Image 4: CTA Close] → animate → [Clip 4: ~1.5-2s]
                                        ↓
                          Stitch in order → Final video (<10s total)
```

Each image is generated to already be "animation-ready" — meaning it's composed with the motion in mind (what will move, what stays static, where text will sit).

---

## Photo 1: The Hook Shot

**Job:** Stop the scroll in under 2 seconds once animated.

**Image generation brief:**
- Subject: A relatable scenario/pain point connected to the product's benefit — NOT the product itself yet
- Composition: Leave upper-third or center clear for hook text overlay
- Style: Candid, UGC-style, natural lighting — avoid studio/stock-photo look
- Framing: Vertical 9:16, subject positioned for a natural push-in or pan

**Animation brief:**
- Motion type: Slow push-in (zoom) OR subtle handheld drift — mimics a phone camera, not a cinematic dolly
- Duration: 1.5–2 seconds
- Avoid: fast zooms, spins, anything that feels "AI-generated-video" artificial

---

## Photo 2: Product Reveal Shot

**Job:** First clear, well-lit look at the actual product.

**Image generation brief:**
- Subject: Product in-hand or in-context, clearly lit, in sharp focus
- Composition: Product should occupy 30-50% of frame, centered or rule-of-thirds
- Background: Simple/uncluttered — avoid busy backgrounds competing with product
- Style: Still UGC-style, but product must be unmistakably the focal point

**Animation brief:**
- Motion type: Hand/product rotation, or a reveal motion (turning to camera, lifting into frame)
- Duration: 2–2.5 seconds
- Avoid: motion that blurs product details — clarity here matters more than dynamism

---

## Photo 3: Proof / Demo Shot

**Job:** The single most convincing "it works" moment.

**Image generation brief:**
- Subject: Product mid-action — the exact moment it does the thing it promises (e.g., switch flipping, device activating)
- Composition: Action point should be visually obvious even as a still frame
- Style: Slightly tighter/closer framing than Photo 2 — this is the "proof" close-up

**Animation brief:**
- Motion type: The demonstrated action itself (press, flip, light turning on, etc.) — this is the one clip where motion IS the content
- Duration: 2.5–3 seconds (longest clip — this beat carries the most weight)
- Avoid: cutting before the action completes

---

## Photo 4: CTA Close Shot

**Job:** Final frame the viewer sees before deciding to buy — must never be dark or ambiguous.

**Image generation brief:**
- Subject: Product clearly displayed, ideally with packaging/branding visible
- Composition: Leave clear space (bottom third typically) for price/offer text overlay
- Lighting: Bright, clean, well-exposed — this is the opposite of a fade-to-black ending
- Style: Slightly more "product shot" polished than the earlier UGC frames — signals credibility at the close

**Animation brief:**
- Motion type: Minimal — slight static hold or very subtle zoom-in. This clip should feel like a "landing," not more movement
- Duration: 1.5–2 seconds
- Critical: last frame of this clip must be sharp, well-lit, and fully legible — this is what freezes on-screen if the viewer pauses

---

## Cross-Cutting Requirements (all 4 images — WITHIN a single video)

*Decision: persona/setting varies per product (not a fixed brand persona across all videos) — but the 4 images within any single video must be internally consistent, per below.*

- **Consistent subject/hands/environment** across all 4 images of the SAME video — if using a generated "person," lock appearance (skin tone, hand, clothing, room) across all 4 prompts for that product so the video doesn't look like 4 different people. This does NOT need to carry over to the next product's video.
- **Consistent lighting direction** across images — mismatched lighting between clips is the #1 tell of AI-stitched content
- **Same product render/asset** used in images 2, 3, and 4 — no variation in product color/shape/label between shots
- **9:16 vertical, matching resolution** across all 4 generations

---

## Text Overlay Zones (reserved space per image)

| Image | Reserved text zone | Content that goes there |
|---|---|---|
| 1. Hook | Upper-third or center | Hook line ("POV: ...") |
| 2. Product Reveal | Lower-third (light) | Optional product name label |
| 3. Proof/Demo | None ideally | Let the action speak — text here competes with proof |
| 4. CTA Close | Lower-third (bold) | Price, offer, "Shop now" cue |

---

## Open Questions to Nail Down Next

- [x] ~~Which image generation model/tool are we using~~ — still open (image gen tool undecided; animation tool is decided)
- [x] Which animation tool — **Kling**, via direct API access
- [ ] Do we need a consistent "creator persona" (same hands/face/voice) across all videos for brand recognition, or should it vary per product?

---

## Kling API — Technical Spec for This Pipeline

**Endpoint:** `POST /v1/videos/image2video` (regional base URL, e.g. `api-singapore.klingai.com`)

**Key parameters:**
| Parameter | Notes for our use |
|---|---|
| `image` | Required. URL or base64 of the source photo (one of our 4 generated beats) |
| `image_tail` | Optional end-frame image — lets us define a start AND end state for the motion (useful for Photo 2 reveal / Photo 3 proof beats) |
| `prompt` | Motion description — maps to the "Animation brief" motion type per beat |
| `negative_prompt` | Use to explicitly exclude fast zooms/spins per our "avoid" notes per beat |
| `duration` | **Fixed to "5" or "10" only** — no custom short durations available |
| `mode` | `"std"` or `"pro"` — use `"pro"` for better motion quality/consistency |
| Camera controls | Explicit params (not just prompt text): horizontal, vertical, pan, tilt, roll, zoom — each on a **-10 to 10 range**. E.g. zoom controls push-in/pull-out directly, more reliable than describing it in the prompt alone |

### ⚠️ Critical workflow implication: duration mismatch

Kling **cannot generate a native 1.5–3 second clip** — minimum output is 5 seconds. Our beat durations (1.5-2s, 2-2.5s, 2.5-3s, 1.5-2s) are all shorter than that. This means the actual pipeline is:

```
Generate each beat at 5s (Kling minimum, mode: pro)
        ↓
Trim in post to the target beat duration from the spec above
        ↓
Stitch the 4 trimmed clips → final video (<10s total)
```

This adds a required **video editing/trimming step** between "animate" and "stitch" that wasn't in the original pipeline diagram — worth remembering when scoping the automation for component #5/#8.

**Cost note:** Kling is priced per-second and is genuinely cheap on paper, but failed/rerolled generations often still consume credits — budget for a ~1.4x multiplier over the sticker price for iteration.



## Final Video Evaluation (applies to the stitched output)

Once the 4 clips are stitched into the final video, run it through this pass/fail filter before it goes live.

### Auto-Disqualifiers (instant reject)
- [ ] Runs 10+ seconds
- [ ] Ends on a black/dark/blank frame
- [ ] More than 2 overlapping text elements at once
- [ ] Product not clearly visible within the first 4 seconds
- [ ] No CTA or price/offer visible in the final frame
- [ ] Inconsistent subject/lighting/product between clips (the "4 different people" problem)

### Scoring Checklist (for tagging in the good/bad examples library)
```
hook_strength: 1-5
product_clarity: 1-5
pacing_cuts: 1-5
text_overlay_clarity: 1-5
cta_presence: yes/no
ending_quality: clean / abrupt / dark-cut
duration_seconds: [value]
verdict: good / bad / borderline
```
