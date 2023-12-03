from fastapi import APIRouter, FastAPI

from ..storage import Coctail, CoctailPartialWithoutId
from .commons import get_storage


def register_coctails_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/coctails", tags=["coctails"])

    @router.get("/")
    async def get_all() -> list[Coctail]:
        return await get_storage(app).get_coctails()

    @router.post("/")
    async def create(coctail: CoctailPartialWithoutId) -> Coctail:
        return await get_storage(app).save_coctail(coctail)

    app.include_router(router)
