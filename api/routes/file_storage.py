from datetime import timedelta
from http import HTTPStatus

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, UploadFile

from ..clients.vercel import BlobUploadResult, blob_upload


def register_file_storage_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/files", tags=["fileStorage"])

    @router.post("/images")
    async def upload(file: UploadFile) -> BlobUploadResult:
        content_type = file.content_type
        if content_type is None or content_type.startswith("image/"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Not an image")
        async with httpx.AsyncClient() as client:
            return await blob_upload(
                client,
                file.filename or "file.bin",
                await file.read(),
                content_type=content_type,
                cache_control_max_age=timedelta(minutes=3),
            )

    app.include_router(router)
