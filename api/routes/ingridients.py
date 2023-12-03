from fastapi import APIRouter, FastAPI, Request

from ..storage import Ingridient, IngridientWithoutId
from .commons import get_storage


def register_ingridients_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/ingridients", tags=["ingridients"])

    @router.get("/")
    async def get_all(request: Request) -> list[Ingridient]:
        return await get_storage(request).get_ingridients()

    @router.post("/")
    async def create(request: Request, ingridient: IngridientWithoutId) -> Ingridient:
        return await get_storage(request).save_ingridient(ingridient)

    app.include_router(router)
