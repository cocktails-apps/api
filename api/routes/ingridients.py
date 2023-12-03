from fastapi import APIRouter, FastAPI

from ..storage import Ingridient, IngridientWithoutId, Storage


def register_ingridients_routes(app: FastAPI, storage: Storage) -> None:
    router = APIRouter(prefix="/ingridients", tags=["ingridients"])

    @router.get("/")
    async def get_all() -> list[Ingridient]:
        return await storage.get_ingridients()

    @router.post("/")
    async def create(ingridient: IngridientWithoutId) -> Ingridient:
        return await storage.save_ingridient(ingridient)

    app.include_router(router)
