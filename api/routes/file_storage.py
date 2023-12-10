import mimetypes
from datetime import timedelta
from http import HTTPStatus
from pathlib import Path
from typing import Optional

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, UploadFile
from typing_extensions import TypeGuard

from ..clients.vercel import BlobUploadResult, blob_upload


def _is_image(file_name: Optional[str]) -> TypeGuard[str]:
    if file_name is None:
        return False

    file_extention = Path(file_name).suffix
    if not file_extention:
        return False

    content_type = mimetypes.types_map.get(file_extention, "")
    return content_type.startswith("image/")


def register_file_storage_routes(app: FastAPI) -> None:
    mimetypes.init()
    router = APIRouter(prefix="/files", tags=["fileStorage"])

    @router.post("/")
    async def upload(file: UploadFile) -> BlobUploadResult:
        async with httpx.AsyncClient() as client:
            file_name = file.filename
            if not _is_image(file_name):
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail="File is not an image",
                )

            return await blob_upload(
                client,
                file_name,
                await file.read(),
                content_type=file.content_type,
                cache_control_max_age=timedelta(minutes=3),
            )

    app.include_router(router)
