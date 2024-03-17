import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TypedDict

from fastapi import FastAPI, Request

from .storage import BlobStorage, local_blob_storage


class State(TypedDict):
    blob_storage: BlobStorage


def blob_storage_from_request(request: Request) -> BlobStorage:
    return request.state.blob_storage  # type: ignore[no-any-return]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[State]:
    local_blob_storage_path = Path(os.environ["LOCAL_BLOB_STORAGE_PATH"])
    with local_blob_storage(local_blob_storage_path) as blob_storage:
        yield {"blob_storage": blob_storage}
