from fastapi import APIRouter, FastAPI, Request

from ..storage import Coctail, CoctailPartialWithoutId
from .commons import get_storage


def register_coctails_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/coctails", tags=["coctails"])

    @router.get("/")
    async def get_all(request: Request) -> list[Coctail]:
        return await get_storage(request).get_coctails()

    @router.post("/")
    async def create(request: Request, coctail: CoctailPartialWithoutId) -> Coctail:
        return await get_storage(request).save_coctail(coctail)

    app.include_router(router)
