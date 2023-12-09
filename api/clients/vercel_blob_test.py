import os
from unittest.mock import patch

from yarl import URL

from .vercel_blob import _get_blob_url


def test_get_blob_url_from_env() -> None:
    with patch.dict(os.environ, {"VERCEL_BLOB_API_URL": "https://some-blob-url.com"}):
        assert _get_blob_url() == URL("https://some-blob-url.com")


def test_get_blob_url_default() -> None:
    with patch.dict(os.environ, clear=True):
        assert _get_blob_url() == URL("https://blob.vercel-storage.com")
