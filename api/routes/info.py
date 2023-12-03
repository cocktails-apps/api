from http import HTTPStatus
from typing import Literal

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from ..storage import is_connected


class HealthResponse(BaseModel):
    status: Literal["OK"] = "OK"


def register_info_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/info")

    @router.get("/health")
    async def health() -> HealthResponse:
        if not await is_connected():
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR, "Not connected to MongoDB"
            )

        return HealthResponse()

    app.include_router(router, include_in_schema=False)
