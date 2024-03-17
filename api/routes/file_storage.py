import mimetypes
from http import HTTPStatus
from pathlib import Path
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import PlainTextResponse
from typing_extensions import TypeGuard

from ..state import blob_storage_from_request


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
        request: Request,
        category: Annotated[Literal["ingridient", "glass", "coctail"], Form()],
        file: UploadFile,
    ) -> PlainTextResponse:
        file_name = file.filename
        if not _is_image(file_name):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="File is not an image",
            )

        blob_storage = blob_storage_from_request(request)
        url = await blob_storage.upload(category, file_name, await file.read())
        return PlainTextResponse(content=str(url))

    app.include_router(router)
