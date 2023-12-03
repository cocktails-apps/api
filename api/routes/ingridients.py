from fastapi import APIRouter, FastAPI

from ..storage import Ingridient, IngridientWithoutId
from .commons import get_storage


def register_ingridients_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/ingridients", tags=["ingridients"])

    @router.get("/")
    async def get_all() -> list[Ingridient]:
        return await get_storage(app).get_ingridients()

    @router.post("/")
    async def create(ingridient: IngridientWithoutId) -> Ingridient:
        return await get_storage(app).save_ingridient(ingridient)

    app.include_router(router)
