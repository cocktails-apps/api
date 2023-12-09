from http import HTTPStatus

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import HTTPException

from ..storage import Coctail, CoctailPartialWithoutId, DocumentNotFound, get_storage


def register_coctails_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/coctails", tags=["coctails"])

    @router.get("/")
    async def get_all() -> list[Coctail]:
        return await get_storage().get_coctails()

    @router.post("/")
    async def create(coctail: CoctailPartialWithoutId) -> Coctail:
        try:
            return await get_storage().save_coctail(coctail)
        except DocumentNotFound as exc:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND) from exc

    app.include_router(router)
