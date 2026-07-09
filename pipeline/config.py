import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-image")

KLING_API_KEY = os.environ.get("KLING_API_KEY")
KLING_BASE_URL = os.environ.get("KLING_BASE_URL", "https://api-singapore.klingai.com")

GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
GCS_SIGNED_URL_EXPIRATION_SECONDS = int(
    os.environ.get("GCS_SIGNED_URL_EXPIRATION_SECONDS", "3600")
)


def require_gemini_key() -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not set. Copy .env.example to .env and fill it in."
        )
    return GEMINI_API_KEY


def require_kling_key() -> str:
    if not KLING_API_KEY:
        raise RuntimeError(
            "KLING_API_KEY not set. Copy .env.example to .env and fill it in."
        )
    return KLING_API_KEY


def require_gcs_bucket() -> str:
    if not GCS_BUCKET_NAME:
        raise RuntimeError(
            "GCS_BUCKET_NAME not set. Copy .env.example to .env and fill it in, "
            "and make sure GOOGLE_APPLICATION_CREDENTIALS points at a service "
            "account key with Storage Object Admin on that bucket."
        )
    return GCS_BUCKET_NAME
