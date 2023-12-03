from fastapi import Request

from ..storage import Storage


def get_storage(request: Request) -> Storage:
    return request.state.storage  # type: ignore[no-any-return]
