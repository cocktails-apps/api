import logging
import os
from datetime import timedelta
from typing import Optional

import httpx
from pydantic import BaseModel, HttpUrl, ValidationError
from yarl import URL

from .blob_errors import BlobError, raise_if_response_failed

logger = logging.getLogger(__name__)


BLOB_API_VERSION = "5"


ENV_BLOB_URL = "VERCEL_BLOB_API_URL"
ENV_BLOB_TOKEN = "BLOB_READ_WRITE_TOKEN"


def _get_blob_api_url() -> URL:
    try:
        base_url = URL(os.environ[ENV_BLOB_URL])
    except KeyError:
        base_url = URL("https://blob.vercel-storage.com")

    return base_url


def _get_token() -> str:
    try:
        return os.environ[ENV_BLOB_TOKEN]
    except KeyError as e:
        raise BlobError(
            f"No token found. Either configure the `{ENV_BLOB_TOKEN}` environment"
            " variable."
        ) from e


class BlobUploadResult(BaseModel):
    url: HttpUrl


async def blob_upload(
    client: httpx.AsyncClient,
    path: str,
    data: bytes,
    *,
    content_type: Optional[str] = None,
    cache_control_max_age: Optional[timedelta] = None,
) -> BlobUploadResult:
    headers = {
        "authorization": f"Bearer {_get_token()}",
        "x-api-version": BLOB_API_VERSION,
        "x-add-random-suffix": "1",
    }

    if content_type is not None:
        logger.debug("Setting content type to %s", content_type)
        headers["x-content-type"] = content_type
    if cache_control_max_age is not None:
        logger.debug("Setting cache control max age to %s", cache_control_max_age)
        headers["x-cache-control-max-age"] = str(cache_control_max_age.total_seconds())

    logger.debug("Uploading %s bytes to %s", len(data), path)
    resp = await client.put(
        f"{_get_blob_api_url()}/{path}", headers=headers, content=data
    )
    raise_if_response_failed(resp)

    try:
        logger.debug("Parsing upload response (%s): %s", resp.status_code, resp.content)
        parsed = BlobUploadResult.model_validate_json(resp.content)
    except ValidationError as e:
        logger.exception("Failed to parse upload response")
        raise BlobError("Can't parse upload response from Blob API") from e

    return parsed
