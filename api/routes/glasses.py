from fastapi import APIRouter, FastAPI

from ..storage import Glass, GlassWithoutId, Storage


def register_glasses_routes(app: FastAPI, storage: Storage) -> None:
    router = APIRouter(prefix="/glasses")

    @router.get("/")
    async def get_all() -> list[Glass]:
        return await storage.get_glasses()

    @router.post("/")
    async def create(glass: GlassWithoutId) -> Glass:
        return await storage.save_glass(glass)

    app.include_router(router)
