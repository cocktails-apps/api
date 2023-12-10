from typing import Literal, Optional

import httpx
from pydantic import BaseModel, ValidationError


class BlobError(RuntimeError):
    pass


class BlobAccessError(BlobError):
    def __init__(self) -> None:
        super().__init__(
            "Access denied, please provide a valid token for this resource"
        )


class BlobStoreNotFoundError(BlobError):
    def __init__(self) -> None:
        super().__init__("This store does not exist")


class BlobStoreSuspendedError(BlobError):
    def __init__(self) -> None:
        super().__init__("This store has been suspended")


class BlobUnknownError(BlobError):
    def __init__(self) -> None:
        super().__init__("Unknown error, please visit https://vercel.com/help")


class BlobServiceNotAvailable(BlobError):
    def __init__(self) -> None:
        super().__init__(
            "The blob service is currently not available. Please try again"
        )


class BlobNotFoundError(BlobError):
    def __init__(self) -> None:
        super().__init__("The requested blob does not exist")


class BlobErrorDescription(BaseModel):
    code: Literal[
        "store_suspended",
        "forbidden",
        "not_found",
        "unknown_error",
        "bad_request",
        "store_not_found",
        "not_allowed",
        "service_unavailable",
    ]
    message: Optional[str] = None


class BlobErrorResponse(BaseModel):
    error: BlobErrorDescription


def raise_if_response_failed(resp: httpx.Response) -> None:
    if resp.is_success:
        return

    try:
        parsed_error = BlobErrorResponse.model_validate_json(resp.content)
        error = parsed_error.error
    except ValidationError as e:
        raise BlobError("Can't parse error response from Blob API") from e

    if error.code == "store_suspended":
        raise BlobStoreSuspendedError()
    if error.code == "forbidden":
        raise BlobAccessError()
    if error.code == "not_found":
        raise BlobNotFoundError()
    if error.code == "store_not_found":
        raise BlobStoreNotFoundError()
    if error.code == "bad_request":
        raise BlobError(error.message or "Bad request")
    if error.code == "service_unavailable":
        raise BlobServiceNotAvailable()

    raise BlobUnknownError()
