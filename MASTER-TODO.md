# MASTER TO-DO — Shopee Affiliate Video AI Pipeline

*Last updated: 2026-07-09*

This is the master tracker for the project. Update status as we complete each stage.

---

## Project Components (in working order)

- [x] **0. Video length constraint locked in** — under 10 seconds, Shopee platform
- [x] **1. Good video requirements** — merged into the image generation doc (scrapped as standalone; structure/scoring/disqualifiers now live in `image-generation-animation-requirements.md`)
- [ ] **2. Good video examples library** — pending real examples + identifier/tagging system
- [ ] **3. Bad video examples library** — 1 example reviewed (switch-genius/Fingerbot video), pending formal tagging using the scoring checklist
- [x] **4. Image generation + animation requirements** — done → `image-generation-animation-requirements.md` (4-photo → 4-clip → stitched video structure, includes final video evaluation checklist)
- [ ] **5. Animate images into video** — in progress: tool decided (Kling API direct). Key finding: Kling image2video only generates 5s or 10s clips (no custom short durations), so pipeline needs a trim-in-post step between animation and stitching. Code scaffolding for both image gen and animation is now written (see `pipeline/` below); next is a live test run once API keys are set.
- [ ] **6. Product selection / featuring process** — parked for now. Shopee's bulk CSV export is category-level only (offer name, commission rate, generic link) — no per-product data (price/orders/rating/image). Decision: hand-pick products manually for now rather than building an automated filtering system prematurely. Revisit once pipeline is producing videos and there's a real need to scale sourcing.
  - **Link generation process (tested, to revisit later):** Shopee Affiliate dashboard → Offer list shows category-level campaigns (e.g. Q1 2026 - Fashion Accessories, Men Clothes, Muslim Fashion, etc.) with commission rates ranging 3-10% depending on category → can select multiple offers via checkboxes → bulk "Get Link" export produces a CSV (`BatchShopeeLinks...csv`) with columns: `Offer Name, Offer Period, Offer Type, Commission Rate, Offer Link` → sample pulled 2026-07-06 had 40 category-level links (10%: Fashion Accessories, Men/Women Clothes, Men/Women Shoes, Muslim Fashion, Travel & Luggage, Bags, Watches, Health & Beauty; 3%: Home Appliances, Mobile & Accessories, Groceries & Pets, Baby & Toys, Gaming & Consoles, Cameras & Drones). This only generates category-level links, not per-product links — once we're ready to scale, need to find the per-product bulk link export (if it exists) or generate links product-by-product for hand-picked items.
- [ ] **7. Video effectiveness analysis** — not started (will need real performance data: views, CTR, conversions)
- [ ] **8. Automated upload pipeline** — not started
- [ ] **9. Audio (sound effects + background music)** — parked, revisit later. Research done 2026-07-09: two separate layers needed. (a) Action sound effects for beats 2/3 — Kling v2.6 (our existing model) has native audio generation built in, frame-synced to motion; `video_gen.py` currently hardcodes `"sound": "off"` per the original brief, flipping to `"on"` is the likely path, but costs more per second (~1.5x based on Kling's credit tiers) and needs a live test. (b) Background music across the full stitched video — separate from Kling, needs a trending/mood-matched music bed mixed in via ffmpeg at the stitch step; Mubert looked like the best fit (API access + sub-licensing built in, which matters since these are commercial affiliate videos, not personal UGC — licensing terms need checking before use). Not blocking anything else; pick back up after the core image→video→stitch pipeline is validated end-to-end.

---

## Immediate Next Steps

1. ~~Decide image generation model/tool~~ — done: Nano Banana 2
2. ~~Decide animation tool~~ — done: Kling (direct API)
3. ~~Decide if we need a consistent "creator persona" across videos or vary per product~~ — done: varies per product, but must stay consistent within each individual video's 4 images
4. ~~Scaffold the pipeline codebase~~ — done: `generate_image()`, `generate_video()`, ffmpeg helpers (`trim_clip`, `zoom_pan_clip`, `stitch_clips`), and `generate_video_from_product()` orchestrator all written (untested against live APIs). See `pipeline/` below.
5. `GEMINI_API_KEY` set locally (`.env`, gitignored) — confirmed **valid and working**: `scripts/test_generate_image.py` authenticated successfully and reached the live API. Currently blocked on **quota**, not auth: `429 RateLimitError — "You do not have enough quota to make this request."` Needs billing/quota enabled on the Google AI Studio / Cloud project this key belongs to before a real image can be generated. `KLING_API_KEY` still needed too.
6. ~~Draft the 4 beat prompts for the validation test product~~ — done, see `products/alpha_borong_switch.py`
7. ~~Generate + validate all 4 test images~~ — done, **visually confirmed good by user 2026-07-09** (hands/lighting/product/room consistency, correct nighttime mood, correct 9:16 aspect ratio). Also caught and fixed two real bugs along the way: (a) aspect ratio wasn't actually being sent to the API (fixed — see Known Gaps below), (b) beats 1-3 prompts contradicted themselves ("night" + "natural window lighting") producing bright daytime renders instead of the intended nighttime scenario — fixed by switching to consistent warm-lamp lighting. Also corrected product identity: the real Shopee listing is "Alpha Borong" branded, not the placeholder "ADAPROX Fingerbot" from the original brief — config renamed, beat 4 packaging text corrected.
8. ~~Run a first test Kling clip~~ — **done and succeeded 2026-07-09.** Beat 2 animated via `kling-v2-6`, std mode, $0.21, 5.04s raw clip (716x1284, h264), sent to user for visual review. Caught and fixed two more real bugs along the way:
   - **Polling URL wrong in the brief**: `GET /v1/videos/{task_id}` 404s. Correct path is `GET /v1/videos/image2video/{task_id}` (confirmed live) — fixed in `video_gen.py`.
   - **ffmpeg wasn't installed in this environment at all** — needed for the trim/stitch steps. Installed via `apt-get update && apt-get install -y ffmpeg`; not yet added to any setup/session-start script, so a fresh environment will hit this again (worth a session-start hook later).
   - Also resolved along the way: Kling account balance was $0 (`code 1102`), user topped it up; this environment's network policy initially blocked both `kling.ai` and `api-singapore.klingai.com` (proxy-level 403s) until the user allowed all domains and started a fresh session (mid-session policy changes don't apply to an already-running proxy).
9. ~~Beat structure restructure~~ — **done 2026-07-09, user decision.** Beat 1 (Hook) now gets real Kling animation (was local zoom/pan), beat 2 (Product Reveal) drops to local zoom/pan (was Kling) — beat 3 stays Kling, beat 4 stays local. Still 2 Kling calls/video, just reassigned. New durations: 3s / 1s / 3s / 1s = **8s total**, deliberately under the 10s hard cap ("people are lazy to watch"). All 4 beats now carry text overlay (beat 3 flips from "no text" to a short instructional line). Full detail in `image-generation-animation-requirements.md`'s update section. `products/alpha_borong_switch.py` and `pipeline/orchestrator.py` updated — `orchestrator.py` is now data-driven (animates via Kling if a beat config has `kling_prompt`, else local zoom/pan) instead of hardcoding which beat numbers get which treatment, so future products can assign differently.
10. ~~Decide + build text overlay tool~~ — **done 2026-07-09**: `ffmpeg`'s `drawtext` filter (`pipeline/ffmpeg_utils.py: add_text_overlay`), no new paid API. Tested live on a real Kling clip, confirmed working (duration preserved, text renders correctly). `overlay_text`/`overlay_zone` are DRAFT copy per beat in `products/alpha_borong_switch.py` — not approved final ad copy, confirm wording before shipping.
11. **Also fixed while restructuring:** `zoom_pan_clip` output (1080x1920) didn't match Kling's raw output resolution (716x1284 confirmed from beat 2) — `stitch_clips` uses `-c copy` (stream copy), which requires identical resolution/codec across all inputs, so concat would likely have failed or produced broken output. Added `ffmpeg_utils.normalize_clip()`, now called on every clip before stitching.
   - **User caught a second bug from this**: `_animate_beat` was burning text onto the raw clip *before* normalization/crop, so text near an edge could get clipped off (Kling's 716x1284 doesn't exactly match the 1080x1920 target, so normalizing crops a thin strip). Fixed by reordering — normalize first, then burn text onto the already-correctly-sized frame. Verified visually: extracted a comparison frame from the old order (text clipped) vs. new order (clean) on the real beat 2 clip.
12. ~~First full end-to-end run~~ — **done and succeeded 2026-07-10.** `final.mp4`: exactly **8.00s**, 1080x1920, h264, all 4 beats stitched with text overlays, sent to user. First orchestrator run hit a transient network error mid-poll (recovered without double-billing by using Kling's list endpoint to resume the already-submitted task) and the `trim_clip` bug below, so the final assembly was completed by re-running the remaining steps manually with the fixes applied rather than a second full orchestrator call — worth re-running `generate_video_from_product()` fresh top-to-bottom once, now that both fixes are in, to confirm it works unattended end-to-end without manual intervention.
    - **Transient network error mid-run**: `ConnectionResetError` while polling beat 1's Kling task, after the job was already submitted and billed ($0.21). Recovered without a duplicate charge by calling Kling's list endpoint (`GET /v1/videos/image2video` with no `task_id`, paginated) to find the still-running task and resume polling it — worth keeping in mind for production: transient network errors mid-poll shouldn't trigger a blind resubmit.
    - **`trim_clip` bug**: used `-c copy` (stream copy) with output-side `-ss`/`-t`, which produced a **0-byte/empty output** on Kling's encoded stream ("Output file is empty, nothing was encoded") — not caught by `check=True` since ffmpeg still exits 0. Fixed: input-side seek (`-ss` before `-i`) + re-encode (`libx264`) instead of stream copy. Confirmed working (72 frames, exact 3.0s) before rolling out.
    - Running total after this run: **$1.33** (9 images + 2 Kling std animations across this session's testing/debugging, not just the final 4-beat/2-animation set a single clean run would cost — a clean run should be ~4 images + 2 Kling std ≈ $0.20 + $0.42 = $0.62).
13. Start tagging more bad/good examples as they come in, using the scoring checklist from the requirements guide
14. Once the single-product pipeline is validated end-to-end, design the product-config data model / batch queue for scaling to many products (component #6 territory) — per-product creative prompts should live in that system (or per-product files), not in this tracker

---

## Open Decisions Log

| Decision | Status | Notes |
|---|---|---|
| Image generation model | **Nano Banana 2** (chosen for cost + strong reference-image consistency support — up to 14 reference images, helps solve the "4 different people" problem) | — |
| Animation tool | **Kling** (chosen for cost — cheapest per-second among major video models) | Component #5. Image-to-video supported; Pro mode 5s/clip cap is fine since our longest beat is ~3s; supports up to 7 reference images for subject/product consistency across clips. Budget for reroll overhead — failed generations can still burn credits, real cost often ~1.4x sticker price. |
| Creator persona consistency | **Varies per product** (Option B) — chosen because product range spans unrelated categories (fashion, electronics, home, beauty); a fixed persona across such different products risked looking templated/fake. Consistency is still required WITHIN each video's 4 images, just not ACROSS different videos. | — |
| Product selection criteria | Parked — hand-picking manually for now | Component #6. Scoring criteria drafted in chat (demonstrable action, simple benefit, sales velocity, $ commission value, rating, visual appeal) — can revisit if/when product-level data sourcing is needed |
| Effectiveness metrics to track | Not discussed | Component #7 — needs Shopee analytics access |

---

## Files Produced So Far

1. `image-generation-animation-requirements.md` — 4-photo generation briefs + animation briefs per beat + final video evaluation checklist (single source of truth, replaces the earlier standalone video requirements guide)
2. `pipeline/` — pipeline codebase: `config.py` (env/API key loading), `image_gen.py` (Nano Banana 2 wrapper), `video_gen.py` (Kling submit + poll wrapper), `ffmpeg_utils.py` (trim/zoom-pan/stitch/normalize/text-overlay), `storage.py` (GCS upload for Kling-reachable URLs + download of Kling results), `orchestrator.py` (`generate_video_from_product`, data-driven per-beat Kling-vs-local animation, wires all beats together), `cost_tracker.py` (logs every image/video API call with estimated cost + running total — see Cost Tracking section below)
3. `products/alpha_borong_switch.py` — single validation test product config, all 4 beat prompts drafted (used to prove the pipeline works end-to-end before scaling to real products; per-product creative content lives here, not in this tracker)
4. `scripts/test_generate_image.py`, `scripts/test_generate_video.py` — standalone test entry points, not yet run (no API keys set in this environment)
5. `requirements.txt`, `.env.example` — dependency list + required env vars (`GEMINI_API_KEY`, `KLING_API_KEY`)

## Cost Tracking

`pipeline/cost_tracker.py` logs every image/video API call to `costs/usage_log.jsonl` (local, gitignored) and prints cost + running total to console on each call.

- **Image cost (Nano Banana 2):** defaulted to $0.05/image (midpoint of the brief's $0.045-$0.055 estimate). Override with `GEMINI_IMAGE_COST_USD` in `.env` once real billing data is available.
- **Video cost (Kling):** **confirmed 2026-07-09** from the official pricing page (`kling.ai/document-api/pricing/base/video`, screenshot provided by user) — `kling-v2-6`, no native audio: **pro mode $0.07/s** ($0.35 per 5s), **std mode $0.042/s** ($0.21 per 5s). Set as `KLING_COST_PER_SECOND_USD_PRO` / `KLING_COST_PER_SECOND_USD_STD` in `.env`. Cost tracker picks the right rate based on which `mode` the actual API call used. `video_gen.py` now explicitly sends `sound="off"` so the real API call matches these pricing tiers. With native audio (component #9, not yet built) this roughly doubles: $0.14/s (no voice control) or $0.168/s (with voice control) in pro mode.
- Kling cost is logged at job submission (not completion) since failed/rerolled jobs can still burn credits per the brief.
- Running total so far: **$0.50** (10 test images generated, 2026-07-09 — includes debugging/regeneration overhead while fixing the aspect-ratio and lighting bugs, not just the final 4-image set)

### Known gaps / unverified assumptions in the current code (flag before relying on it)
- ~~`aspect_ratio` parameter placement was a guess~~ — **fixed 2026-07-09**: `generation_config.image_config.aspect_ratio` is deprecated in the installed SDK; the working path is `response_format={"type": "image", "aspect_ratio": ..., "image_size": "1K"}`, passed directly to `client.interactions.create()`. Confirmed live: reference-based generations were drifting to a different resolution (848x1264 vs 768x1376) before this fix, now consistent across all 4 beats.
- `video_gen.py` assumes a simple `Authorization: Bearer <token>` auth scheme per the brief; some Kling accounts use JWT-based auth instead — verify against your actual account's docs
- ~~orchestrator's beat 2/3 flow needed an upload-before-Kling and download-before-trim step~~ — **fixed 2026-07-09**: wired through `pipeline/storage.py` (GCS)
- ~~`storage.upload_file()` signed-URL generation unverified~~ — **confirmed working live 2026-07-09**: bucket `mike-affiliate-video-assets` + service account credentials tested end-to-end (upload → signed URL → HTTP 200 fetch, content-length matched). All 3 API integrations (Gemini, Kling key set, GCS) now have working credentials.

---

*This file should live in Project Knowledge as the pinned master reference — update the checkboxes and log as each component gets built out.*
