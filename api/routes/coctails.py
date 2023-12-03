from fastapi import APIRouter, FastAPI

from ..storage import Coctail, CoctailPartialWithoutId, get_storage


def register_coctails_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/coctails", tags=["coctails"])

    @router.get("/")
    async def get_all() -> list[Coctail]:
        return await get_storage().get_coctails()

    @router.post("/")
    async def create(coctail: CoctailPartialWithoutId) -> Coctail:
        return await get_storage().save_coctail(coctail)

    app.include_router(router)
