from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .routes import (
    register_coctails_routes,
    register_glasses_routes,
    register_info_routes,
    register_ingridients_routes,
)
from .storage import get_storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.storage = get_storage()

    yield


app = FastAPI(lifespan=lifespan)
register_info_routes(app)
register_coctails_routes(app)
register_glasses_routes(app)
register_ingridients_routes(app)
