import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

LOG_PATH = os.path.join("costs", "usage_log.jsonl")

# Gemini image pricing per the handoff brief: ~$0.045-$0.055/image, provider-
# dependent. Using the midpoint as a default estimate — override with the
# real figure from your billing page once you have one.
GEMINI_IMAGE_COST_USD = float(os.environ.get("GEMINI_IMAGE_COST_USD", "0.05"))

# Kling pricing confirmed 2026-07-09 from the official pricing page
# (kling-v2-6): pro mode $0.07/s, std mode $0.042/s. Rate depends on which
# mode a given call actually used, not just the model — cost is unknown
# until the matching env var is set, rather than silently guessing.
_kling_pro_env = os.environ.get("KLING_COST_PER_SECOND_USD_PRO")
KLING_COST_PER_SECOND_USD_PRO = float(_kling_pro_env) if _kling_pro_env else None

_kling_std_env = os.environ.get("KLING_COST_PER_SECOND_USD_STD")
KLING_COST_PER_SECOND_USD_STD = float(_kling_std_env) if _kling_std_env else None

_KLING_RATES_BY_MODE = {
    "pro": KLING_COST_PER_SECOND_USD_PRO,
    "std": KLING_COST_PER_SECOND_USD_STD,
}


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


def log_video_call(model: str, seconds: float, mode: str = "pro") -> dict:
    rate = _KLING_RATES_BY_MODE.get(mode)
    if rate is None:
        entry = _append(
            {
                "type": "video",
                "model": model,
                "mode": mode,
                "units_seconds": seconds,
                "estimated_cost_usd": None,
                "note": f"KLING_COST_PER_SECOND_USD_{mode.upper()} not set - "
                "cost unknown. Set it in .env from Kling's pricing page.",
            }
        )
    else:
        cost = round(rate * seconds, 4)
        entry = _append(
            {
                "type": "video",
                "model": model,
                "mode": mode,
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
