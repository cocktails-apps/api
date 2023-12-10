from unittest.mock import create_autospec

import httpx
import pytest

from .blob_errors import (
    BlobAccessError,
    BlobError,
    BlobErrorDescription,
    BlobErrorResponse,
    BlobNotFoundError,
    BlobServiceNotAvailable,
    BlobStoreNotFoundError,
    BlobStoreSuspendedError,
    BlobUnknownError,
    raise_if_response_failed,
)


@pytest.fixture
def response() -> httpx.Response:
    r = create_autospec(httpx.Response, spec_set=True, instance=True)
    r.is_success = False
    return r


def test_raise_if_response_failed_success(response: httpx.Response) -> None:
    response.is_success = True
    raise_if_response_failed(response)


def test_raise_if_response_failed_parse_error(response: httpx.Response) -> None:
    response.content = b"not json"
    with pytest.raises(BlobError, match="Can't parse error response from Blob API"):
        raise_if_response_failed(response)


@pytest.mark.parametrize(
    ("error_description", "expected"),
    [
        (BlobErrorDescription(code="store_suspended"), BlobStoreSuspendedError),
        (BlobErrorDescription(code="forbidden"), BlobAccessError),
        (BlobErrorDescription(code="not_found"), BlobNotFoundError),
        (BlobErrorDescription(code="store_not_found"), BlobStoreNotFoundError),
        (
            BlobErrorDescription(code="bad_request", message="some error message"),
            BlobError,
        ),
        (BlobErrorDescription(code="service_unavailable"), BlobServiceNotAvailable),
        (BlobErrorDescription(code="unknown_error"), BlobUnknownError),
    ],
)
def test_raise_if_response_failed(
    response: httpx.Response,
    error_description: BlobErrorDescription,
    expected: type[Exception],
) -> None:
    response.content = (
        BlobErrorResponse(error=error_description).model_dump_json().encode()
    )
    with pytest.raises(expected):
        raise_if_response_failed(response)
