# MASTER TO-DO — Shopee Affiliate Video AI Pipeline

*Last updated: 2026-07-06*

This is the master tracker for the project. Update status as we complete each stage.

---

## Project Components (in working order)

- [x] **0. Video length constraint locked in** — under 10 seconds, Shopee platform
- [x] **1. Good video requirements** — merged into the image generation doc (scrapped as standalone; structure/scoring/disqualifiers now live in `image-generation-animation-requirements.md`)
- [ ] **2. Good video examples library** — pending real examples + identifier/tagging system
- [ ] **3. Bad video examples library** — 1 example reviewed (switch-genius/Fingerbot video), pending formal tagging using the scoring checklist
- [x] **4. Image generation + animation requirements** — done → `image-generation-animation-requirements.md` (4-photo → 4-clip → stitched video structure, includes final video evaluation checklist)
- [ ] **5. Animate images into video** — in progress: tool decided (Kling API direct). Key finding: Kling image2video only generates 5s or 10s clips (no custom short durations), so pipeline needs a trim-in-post step between animation and stitching. Next: write actual per-beat prompts + camera control params.
- [ ] **6. Product selection / featuring process** — parked for now. Shopee's bulk CSV export is category-level only (offer name, commission rate, generic link) — no per-product data (price/orders/rating/image). Decision: hand-pick products manually for now rather than building an automated filtering system prematurely. Revisit once pipeline is producing videos and there's a real need to scale sourcing.
  - **Link generation process (tested, to revisit later):** Shopee Affiliate dashboard → Offer list shows category-level campaigns (e.g. Q1 2026 - Fashion Accessories, Men Clothes, Muslim Fashion, etc.) with commission rates ranging 3-10% depending on category → can select multiple offers via checkboxes → bulk "Get Link" export produces a CSV (`BatchShopeeLinks...csv`) with columns: `Offer Name, Offer Period, Offer Type, Commission Rate, Offer Link` → sample pulled 2026-07-06 had 40 category-level links (10%: Fashion Accessories, Men/Women Clothes, Men/Women Shoes, Muslim Fashion, Travel & Luggage, Bags, Watches, Health & Beauty; 3%: Home Appliances, Mobile & Accessories, Groceries & Pets, Baby & Toys, Gaming & Consoles, Cameras & Drones). This only generates category-level links, not per-product links — once we're ready to scale, need to find the per-product bulk link export (if it exists) or generate links product-by-product for hand-picked items.
- [ ] **7. Video effectiveness analysis** — not started (will need real performance data: views, CTR, conversions)
- [ ] **8. Automated upload pipeline** — not started

---

## Immediate Next Steps

1. ~~Decide image generation model/tool~~ — done: Nano Banana 2
2. ~~Decide animation tool~~ — done: Kling (direct API)
3. ~~Decide if we need a consistent "creator persona" across videos or vary per product~~ — done: varies per product, but must stay consistent within each individual video's 4 images
4. Write actual Nano Banana 2 prompts for the 4 beats (Hook, Product Reveal, Proof/Demo, CTA Close), using its reference-image feature to lock subject/hands/product/lighting consistency across all 4 images of ONE video
5. Generate a first test image (1 of the 4 beats) to validate the requirements doc
6. Once all 4 test images look right, generate a first test Kling clip (beat 2 or 3) to validate the animation step
7. Start tagging more bad/good examples as they come in, using the scoring checklist from the requirements guide

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

---

*This file should live in Project Knowledge as the pinned master reference — update the checkboxes and log as each component gets built out.*
