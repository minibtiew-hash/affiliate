# Image Generation + Animation Requirements
### Pipeline: 4 Photos → 4 Animated Clips → 1 Stitched Video (<10s)

This spec defines what to generate at the **image stage**, so that each image already carries everything it needs before animation.

---

## ⚠️ 2026-07-09 update — beat structure revised (supersedes durations/animation assignment below)

User decision, applied to the `alpha_borong_switch` product config and the orchestrator:

| Beat | Animation | Duration | Text overlay |
|---|---|---|---|
| 1. Hook | **Kling** (was local) | 3s | Yes — POV line, upper-third |
| 2. Product Reveal | **Local zoom/pan** (was Kling) | 1s | Yes, light — product name, lower-third |
| 3. Proof/Demo | Kling (unchanged) | 3s | Yes — short "how to use" line (was "none ideally") |
| 4. CTA Close | Local zoom/pan (unchanged) | 1s | Yes, bold — NOT "buy now"/price, a benefit line instead (e.g. "don't need to stand up again"), lower-third |

**Total target ~8s, not the full 10s** — reasoning: shorter clips hold attention better, viewers are "lazy to watch." Still only 2 Kling calls per video (beats 1 & 3 now, was 2 & 3), so the cost-optimization intent from the original brief is preserved, just reassigned.

Text overlays are burned in via `ffmpeg`'s `drawtext` filter (`pipeline/ffmpeg_utils.py: add_text_overlay`) — no paid API, reuses the existing local toolchain. All 4 beats now carry overlay text (beat 3 flips from the original "no text" guidance since the user wants a short instructional line there).

---

## Pipeline Overview (original — see table above for current assignment)

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

### ⚠️ Demo beat realism principles (added 2026-07-10 — apply to EVERY product's beat 3)

The first end-to-end video's demo beat read as unrealistic/CGI. Diagnosis on the real output, generalized so every future product's demo prompt follows these rules:

1. **Show the human trigger in-frame.** An action with no visible cause (a device operating "by itself") reads as fake. Compose the still so cause and effect are both visible in one frame — the finger on the button/remote in the foreground, the product acting in the mid-ground. The viewer must see *who* initiated the action.
2. **Never ask the video model for a scene state change.** "Light turns on," "liquid appears," "color changes" are where AI video morphs and warps worst. Set the scene state in the *still image* (lamp already on) and animate only physical motion. If a before→after state is truly essential, use Kling's `image_tail` (explicit end frame) rather than describing the change in the prompt text.
3. **Animate ONE small, mechanical motion — and explicitly anchor everything else.** Say exactly what moves ("the thumb presses the button once," "the arm pushes down with one short movement") *and* explicitly state that everything else stays still: camera static, lighting unchanged, hand in place. Unanchored prompts make Kling drift everything slightly, which reads as dreamlike, not real.
4. **Lock the camera for demo beats.** A propped-phone, completely static camera is the UGC realism baseline — camera motion stacked on object motion compounds artifacts. Put "camera movement, zoom, pan" in the negative prompt.
5. **Negative-prompt the classic AI tells**: morphing, warping, object deformation, extra fingers, hand distortion, light flicker.

Reference implementation: `products/alpha_borong_switch.py` beat 3 (revised 2026-07-10).

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
| 2. Product Reveal | Lower-third (light) | "Now introducing..." + product name — must explicitly signal to the viewer that THIS is the product being sold, not just name it |
| 3. Proof/Demo | None ideally | Let the action speak — text here competes with proof |
| 4. CTA Close | Lower-third (bold) | Price, offer, "Shop now" cue |

### ⚠️ Text overlay rules for 9:16 mobile (added 2026-07-14 — apply to EVERY video)

Found live: caption text was running off the frame edges and sitting under platform UI. These rules are implemented in `pipeline/ffmpeg_utils.py` and apply universally:

1. **Respect the mobile UI safe area.** Shopee/TikTok-style players cover roughly the **top ~8%** (status/search bar), **bottom ~22%** (caption, buttons, progress bar), and **right ~15%** (like/share/cart action rail). No burned-in text may sit in those bands. Current safe zone anchors: upper text at y≈0.16, lower text at y≈0.64–0.68 — never lower.
2. **Always wrap text — never render one long line.** ffmpeg's `drawtext` does not wrap on its own; an unwrapped hook line rendered ~1600px wide on a 1080px frame. Max line width is ~80% of frame width, auto-wrapped onto multiple lines (`_wrap_for_width`).
3. **Use a real social-caption font, never a default system font.** Default fonts (DejaVu etc.) read as "AI-generated." Standard is **Poppins ExtraBold** (`assets/fonts/`, OFL-licensed for commercial use) with a thick dark border — the native TikTok/Shopee caption look.
4. **Verify with a frame extract, not just a successful render.** Pull a frame (`ffmpeg -ss ... -frames:v 1`) and check text position/wrapping/glyphs before shipping — escaping bugs (e.g. a swallowed apostrophe) and clipping don't fail the render, they just look wrong.

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
