from fastapi import APIRouter, FastAPI

from ..storage import Coctail, CoctailPartialWithoutId, Storage


def register_coctails_routes(app: FastAPI, storage: Storage) -> None:
    router = APIRouter(prefix="/coctails", tags=["coctails"])

    @router.get("/")
    async def get_all() -> list[Coctail]:
        return await storage.get_coctails()

    @router.post("/")
    async def create(coctail: CoctailPartialWithoutId) -> Coctail:
        return await storage.save_coctail(coctail)

    app.include_router(router)
