import os
from datetime import timedelta
from typing import Optional
from unittest.mock import create_autospec, patch

import httpx
import pytest
from yarl import URL

from .blob import BlobUploadResult, _get_blob_api_url, _get_token, blob_upload
from .blob_errors import BlobError


def test_get_blob_api_url_from_env() -> None:
    with patch.dict(os.environ, {"VERCEL_BLOB_API_URL": "https://some-blob-url.com"}):
        assert _get_blob_api_url() == URL("https://some-blob-url.com")


def test_get_blob_api_url_default() -> None:
    with patch.dict(os.environ, clear=True):
        assert _get_blob_api_url() == URL("https://blob.vercel-storage.com")


def test_get_token_in_env() -> None:
    with patch.dict(os.environ, {"BLOB_READ_WRITE_TOKEN": "some-token"}):
        assert _get_token() == "some-token"


def test_get_token_not_in_env() -> None:
    with patch.dict(os.environ, clear=True):

        with pytest.raises(BlobError, match="No token found"):
            _get_token()


@pytest.fixture
def client() -> httpx.AsyncClient:
    return create_autospec(httpx.AsyncClient, spec_set=True, instance=True)


@pytest.fixture
def api_url() -> URL:
    with patch(
        "api.clients.vercel.blob._get_blob_api_url",
        return_value=URL("https://some-api.vercel"),
    ) as m:
        yield m.return_value


@pytest.fixture
def blob_token() -> str:
    with patch(
        "api.clients.vercel.blob._get_token",
        return_value="some-token",
    ) as m:
        yield m.return_value


@pytest.fixture
def response() -> httpx.Response:
    r = create_autospec(httpx.Response, instance=True)
    r.is_success = True
    r.status_code = 200
    return r


@pytest.mark.parametrize(
    ("content_type", "max_age"),
    [
        pytest.param(
            "some/content-type", timedelta(days=1), id="with content type and max age"
        ),
        pytest.param("some/content-type", None, id="with content type and no max age"),
        pytest.param(None, timedelta(days=1), id="with no content type and max age"),
        pytest.param(None, None, id="with no content type and no max age"),
    ],
)
async def test_blob_upload(
    client: httpx.AsyncClient,
    api_url: URL,
    blob_token: str,
    response: httpx.Response,
    content_type: Optional[str],
    max_age: Optional[timedelta],
) -> None:
    path = "some-path"
    data = b"some data"

    response.content = (
        BlobUploadResult(url="https://some-url.com", path=path)
        .model_dump_json()
        .encode()
    )
    client.put.return_value = response

    res = await blob_upload(
        client, path, data, content_type=content_type, cache_control_max_age=max_age
    )

    client.put.assert_called_once()
    call = client.put.mock_calls[0]
    assert call.args[0] == str(api_url / path)
    headers = call.kwargs["headers"]
    assert headers["authorization"] == f"Bearer {blob_token}"
    assert headers["x-api-version"] == "5"
    assert headers["x-add-random-suffix"] == "1"
    if content_type is not None:
        assert headers["x-content-type"] == content_type
    else:
        assert "x-content-type" not in headers

    if max_age is not None:
        assert headers["x-cache-control-max-age"] == str(max_age.total_seconds())
    else:
        assert "x-cache-control-max-age" not in headers

    assert str(res.url) == "https://some-url.com/"
    assert res.path == path


async def test_blob_upload_parse_response_failure(
    client: httpx.AsyncClient, api_url: URL, blob_token: str, response: httpx.Response
) -> None:
    response.content = b"some invalid json"
    with pytest.raises(BlobError, match="Can't parse upload response from Blob API"):
        await blob_upload(client, "some-path", b"some data")
