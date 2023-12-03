from fastapi import APIRouter, FastAPI

from ..storage import Glass, GlassWithoutId
from .commons import get_storage


def register_glasses_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/glasses", tags=["glasses"])

    @router.get("/")
    async def get_all() -> list[Glass]:
        return await get_storage(app).get_glasses()

    @router.post("/")
    async def create(glass: GlassWithoutId) -> Glass:
        return await get_storage(app).save_glass(glass)

    app.include_router(router)
