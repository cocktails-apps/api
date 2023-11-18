from typing import Literal

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["OK"] = "OK"


def register_info_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/info")

    @router.get("/health")
    def health() -> HealthResponse:
        return HealthResponse()

    app.include_router(router, include_in_schema=False)
