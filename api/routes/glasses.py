from fastapi import APIRouter, FastAPI, Request

from ..storage import Glass, GlassWithoutId
from .commons import get_storage


def register_glasses_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/glasses", tags=["glasses"])

    @router.get("/")
    async def get_all(request: Request) -> list[Glass]:
        return await get_storage(request).get_glasses()

    @router.post("/")
    async def create(request: Request, glass: GlassWithoutId) -> Glass:
        return await get_storage(request).save_glass(glass)

    app.include_router(router)
