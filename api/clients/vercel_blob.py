import os

from yarl import URL

BLOB_API_VERSION = 5


def _get_blob_url() -> URL:
    try:
        base_url = URL(os.environ["VERCEL_BLOB_API_URL"])
    except KeyError:
        base_url = URL("https://blob.vercel-storage.com")

    return base_url
