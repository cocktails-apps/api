from datetime import timedelta

import httpx
from fastapi import APIRouter, FastAPI, UploadFile

from ..clients.vercel import BlobUploadResult, blob_upload


def register_file_storage_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/files", tags=["fileStorage"])

    @router.post("/")
    async def upload(file: UploadFile) -> BlobUploadResult:
        async with httpx.AsyncClient() as client:
            return await blob_upload(
                client,
                file.filename,
                await file.read(),
                content_type=file.content_type,
                cache_control_max_age=timedelta(minutes=3),
            )

    app.include_router(router)
