from http import HTTPStatus
from typing import Literal

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["OK"] = "OK"


def register_info_routes(app: FastAPI, mongo_client: AsyncIOMotorClient) -> None:
    router = APIRouter(prefix="/info")

    @router.get("/health")
    async def health() -> HealthResponse:
        try:
            await mongo_client.server_info()
            return HealthResponse()
        except Exception:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR, "Not connected to MongoDB"
            )

    app.include_router(router, include_in_schema=False)
