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

---

## Immediate Next Steps

1. ~~Decide image generation model/tool~~ — done: Nano Banana 2
2. ~~Decide animation tool~~ — done: Kling (direct API)
3. ~~Decide if we need a consistent "creator persona" across videos or vary per product~~ — done: varies per product, but must stay consistent within each individual video's 4 images
4. ~~Scaffold the pipeline codebase~~ — done: `generate_image()`, `generate_video()`, ffmpeg helpers (`trim_clip`, `zoom_pan_clip`, `stitch_clips`), and `generate_video_from_product()` orchestrator all written (untested against live APIs). See `pipeline/` below.
5. `GEMINI_API_KEY` set locally (`.env`, gitignored) — confirmed **valid and working**: `scripts/test_generate_image.py` authenticated successfully and reached the live API. Currently blocked on **quota**, not auth: `429 RateLimitError — "You do not have enough quota to make this request."` Needs billing/quota enabled on the Google AI Studio / Cloud project this key belongs to before a real image can be generated. `KLING_API_KEY` still needed too.
6. Draft the 3 remaining Fingerbot prompts (beats 1, 3, 4 — only beat 2 is written, in `products/fingerbot.py`)
7. Re-run `scripts/test_generate_image.py` once quota is sorted, to generate the first real test image (Fingerbot beat 2), validate visually
8. Once all 4 test images look right, run a first test Kling clip (beat 2 or 3) via `scripts/test_generate_video.py` to validate the animation step — note this needs the generated image hosted at a reachable URL first (Kling doesn't accept local file paths)
9. Run one full end-to-end test via `generate_video_from_product()` on the Fingerbot case
10. Start tagging more bad/good examples as they come in, using the scoring checklist from the requirements guide

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
2. `pipeline/` — pipeline codebase: `config.py` (env/API key loading), `image_gen.py` (Nano Banana 2 wrapper), `video_gen.py` (Kling submit + poll wrapper), `ffmpeg_utils.py` (trim/zoom-pan/stitch), `orchestrator.py` (`generate_video_from_product`, wires all beats together)
3. `products/fingerbot.py` — test product config; beat 2 prompt drafted from the brief, beats 1/3/4 still TODO
4. `scripts/test_generate_image.py`, `scripts/test_generate_video.py` — standalone test entry points, not yet run (no API keys set in this environment)
5. `requirements.txt`, `.env.example` — dependency list + required env vars (`GEMINI_API_KEY`, `KLING_API_KEY`)

### Known gaps / unverified assumptions in the current code (flag before relying on it)
- `image_gen.py` follows the brief's documented `client.interactions.create` SDK call verbatim — not yet confirmed against a live response, and the exact `aspect_ratio` parameter placement is still a guess (marked TODO in code)
- `video_gen.py` assumes a simple `Authorization: Bearer <token>` auth scheme per the brief; some Kling accounts use JWT-based auth instead — verify against your actual account's docs
- `orchestrator.py`'s beat 2/3 flow calls `trim_clip` directly on the Kling result URL — a download-to-local-file step is still needed before trimming works (noted as a TODO in the code); also Kling's `image` field needs a hosted URL, not a local path, so generated PNGs need an upload step before being sent to Kling

---

*This file should live in Project Knowledge as the pinned master reference — update the checkboxes and log as each component gets built out.*
