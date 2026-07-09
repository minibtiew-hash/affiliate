import json
import os
from datetime import datetime, timezone

LOG_PATH = os.path.join("costs", "usage_log.jsonl")

# Gemini image pricing per the handoff brief: ~$0.045-$0.055/image, provider-
# dependent. Using the midpoint as a default estimate — override with the
# real figure from your billing page once you have one.
GEMINI_IMAGE_COST_USD = float(os.environ.get("GEMINI_IMAGE_COST_USD", "0.05"))

# Kling has no sticker price in the brief (only "budget ~1.4x for rerolls").
# Cost stays unknown/unlogged until you set this from your actual billing
# page — better to say "unknown" than to silently guess wrong.
_kling_env = os.environ.get("KLING_COST_PER_SECOND_USD")
KLING_COST_PER_SECOND_USD = float(_kling_env) if _kling_env else None


def _append(entry: dict) -> dict:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def log_image_call(model: str, count: int = 1) -> dict:
    cost = round(GEMINI_IMAGE_COST_USD * count, 4)
    entry = _append(
        {
            "type": "image",
            "model": model,
            "units": count,
            "estimated_cost_usd": cost,
            "cost_is_estimate": True,
        }
    )
    _print_entry(entry)
    return entry


def log_video_call(model: str, seconds: float) -> dict:
    if KLING_COST_PER_SECOND_USD is None:
        entry = _append(
            {
                "type": "video",
                "model": model,
                "units_seconds": seconds,
                "estimated_cost_usd": None,
                "note": "KLING_COST_PER_SECOND_USD not set - cost unknown. "
                "Set it in .env from your Kling billing page.",
            }
        )
    else:
        cost = round(KLING_COST_PER_SECOND_USD * seconds, 4)
        entry = _append(
            {
                "type": "video",
                "model": model,
                "units_seconds": seconds,
                "estimated_cost_usd": cost,
                "cost_is_estimate": True,
            }
        )
    _print_entry(entry)
    return entry


def running_total() -> float:
    total = 0.0
    if not os.path.exists(LOG_PATH):
        return total
    with open(LOG_PATH) as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("estimated_cost_usd") is not None:
                total += entry["estimated_cost_usd"]
    return round(total, 4)


def _print_entry(entry: dict) -> None:
    if entry.get("estimated_cost_usd") is None:
        print(f"[cost] {entry['type']} call ({entry['model']}): cost unknown — {entry.get('note', '')}")
        return
    tag = " (estimate)" if entry.get("cost_is_estimate") else ""
    print(
        f"[cost] {entry['type']} call ({entry['model']}): "
        f"${entry['estimated_cost_usd']:.4f}{tag} | running total: ${running_total():.4f}"
    )
