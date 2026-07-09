import os
from datetime import timedelta

import requests
from google.cloud import storage

from pipeline import config

_client = None


def _get_client() -> storage.Client:
    global _client
    if _client is None:
        _client = storage.Client()
    return _client


def upload_file(local_path: str, dest_blob_name: str | None = None) -> str:
    """Upload a local file to GCS, return a signed URL Kling can fetch.

    Requires GOOGLE_APPLICATION_CREDENTIALS pointed at a service account key
    with signing permission (plain Application Default Credentials from
    `gcloud auth login` generally can't sign URLs).
    """
    bucket_name = config.require_gcs_bucket()
    dest_blob_name = dest_blob_name or os.path.basename(local_path)

    bucket = _get_client().bucket(bucket_name)
    blob = bucket.blob(dest_blob_name)
    blob.upload_from_filename(local_path)

    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=config.GCS_SIGNED_URL_EXPIRATION_SECONDS),
        method="GET",
    )


def download_file(url: str, local_path: str) -> str:
    os.makedirs(os.path.dirname(local_path) or ".", exist_ok=True)
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(local_path, "wb") as f:
        f.write(response.content)
    return local_path
