import os
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, Request

from ..storage import BlobStorage, local_blob_storage, vercel_blob_storage


def http_client_from_request(request: Request) -> httpx.AsyncClient:
    return request.state.http_client  # type: ignore[no-any-return]


def blob_storage_from_request(request: Request) -> BlobStorage:
    return request.state.blob_storage  # type: ignore[no-any-return]


def register_state_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def _(request: Request, call_next: Any) -> Any:
        is_vercel = bool(os.environ.get("VERCEL"))

        async with httpx.AsyncClient() as http_client:
            request.state.http_client = http_client

            if is_vercel:
                request.state.blob_storage = vercel_blob_storage(
                    http_client,
                    os.environ["VERCEL_ENV"],
                )
                return await call_next(request)

            local_blob_storage_path = Path(os.environ["LOCAL_BLOB_STORAGE_PATH"])
            with local_blob_storage(local_blob_storage_path) as blob_storage:
                request.state.blob_storage = blob_storage
                return await call_next(request)
