import time

import requests

from pipeline import config, cost_tracker

TERMINAL_STATUSES = {"succeed", "completed", "failed"}


def generate_video(
    image_path_or_url: str,
    prompt: str,
    negative_prompt: str = "",
    image_tail: str | None = None,
    camera_params: dict | None = None,
    duration: str = "5",
    mode: str = "pro",
    poll_interval: int = 5,
    timeout: int = 600,
) -> str:
    """Submit an image2video job to Kling, poll until done, return the clip URL.

    duration must stay "5" (Kling's minimum) — trimming to the beat's real
    target length happens afterwards via ffmpeg_utils.trim_clip.
    """
    api_key = config.require_kling_key()
    headers = {"Authorization": f"Bearer {api_key}"}

    body = {
        "model_name": "kling-v2-6",
        "image": image_path_or_url,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "duration": duration,
        "mode": mode,
    }
    if image_tail:
        body["image_tail"] = image_tail
    for key, value in (camera_params or {}).items():
        if not -10 <= value <= 10:
            raise ValueError(f"camera param {key}={value} out of range [-10, 10]")
        body[key] = value

    submit = requests.post(
        f"{config.KLING_BASE_URL}/v1/videos/image2video",
        headers=headers,
        json=body,
        timeout=30,
    )
    submit.raise_for_status()
    task_id = submit.json()["data"]["task_id"]

    # Kling bills per second of generated output as soon as a job is
    # accepted — even failed/rerolled jobs can still consume credits (per
    # the brief's ~1.4x budgeting note) — so log cost here, not on success.
    cost_tracker.log_video_call(model=body["model_name"], seconds=float(duration))

    deadline = time.time() + timeout
    while time.time() < deadline:
        poll = requests.get(
            f"{config.KLING_BASE_URL}/v1/videos/{task_id}",
            headers=headers,
            timeout=30,
        )
        poll.raise_for_status()
        data = poll.json()["data"]
        status = data["task_status"]

        if status in ("succeed", "completed"):
            return data["task_result"]["videos"][0]["url"]
        if status == "failed":
            raise RuntimeError(f"Kling task {task_id} failed: {data.get('task_status_msg')}")

        time.sleep(poll_interval)

    raise TimeoutError(f"Kling task {task_id} did not finish within {timeout}s")
