from http import HTTPStatus
from sys import version
from typing import Literal

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from ..storage import is_connected


class HealthResponse(BaseModel):
    status: Literal["OK"] = "OK"


class VersionsResponse(BaseModel):
    python: str = version


def register_info_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/info", tags=["info"])

    @router.get("/health")
    async def health() -> HealthResponse:
        if not await is_connected():
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR, "Not connected to MongoDB"
            )

        return HealthResponse()

    @router.get("/versions")
    async def version() -> VersionsResponse:
        return VersionsResponse()

    app.include_router(router)
