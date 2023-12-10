import mimetypes
from datetime import timedelta
from http import HTTPStatus
from pathlib import Path
from typing import Literal, Optional

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, UploadFile
from typing_extensions import TypeGuard

from ..clients.vercel import BlobUploadResult, blob_upload

CACHE_CONTROL_MAX_AGE = timedelta(minutes=3)


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
    async def upload(
        category: Literal["ingridient", "glass", "coctail"], file: UploadFile
    ) -> BlobUploadResult:
        async with httpx.AsyncClient() as client:
            file_name = file.filename
            if not _is_image(file_name):
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail="File is not an image",
                )

            return await blob_upload(
                client,
                f"{category}/{file_name}",
                await file.read(),
                cache_control_max_age=CACHE_CONTROL_MAX_AGE,
            )

    app.include_router(router)
