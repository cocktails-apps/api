from fastapi import APIRouter, FastAPI

from ..storage import Coctail, Storage


def register_coctails_routes(app: FastAPI, storage: Storage) -> None:
    router = APIRouter(prefix="/coctails")

    @router.get("/")
    async def get() -> list[Coctail]:
        return await storage.get_coctails()

    app.include_router(router)
