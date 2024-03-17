import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

import httpx
from fastapi import FastAPI, Request

from .storage import BlobStorage, local_blob_storage, vercel_blob_storage


class State(TypedDict):
    http_client: httpx.AsyncClient
    blob_storage: BlobStorage


def http_client_from_request(request: Request) -> httpx.AsyncClient:
    return request.state.http_client  # type: ignore[no-any-return]


def blob_storage_from_request(request: Request) -> BlobStorage:
    return request.state.blob_storage  # type: ignore[no-any-return]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[State]:
    is_vercel = bool(os.environ.get("VERCEL"))

    if TYPE_CHECKING:
        blob_storage: BlobStorage

    async with httpx.AsyncClient() as http_client:
        if is_vercel:
            blob_storage = vercel_blob_storage(
                http_client,
                os.environ["VERCEL_ENV"],
            )
            yield {
                "http_client": http_client,
                "blob_storage": blob_storage,
            }
        else:
            local_blob_storage_path = Path(os.environ["LOCAL_BLOB_STORAGE_PATH"])
            with local_blob_storage(local_blob_storage_path) as blob_storage:
                yield {
                    "http_client": http_client,
                    "blob_storage": blob_storage,
                }
