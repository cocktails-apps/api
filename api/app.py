import os

from fastapi import FastAPI

from .log import configure_logger
from .middleware import register_cors_middleware
from .routes import (
    register_coctails_routes,
    register_file_storage_routes,
    register_glasses_routes,
    register_info_routes,
    register_ingridients_routes,
)

debug = os.environ.get("DEBUG", "0").lower() != "0"

configure_logger(debug)

app = FastAPI(
    debug=debug,
    docs_url="/docs" if debug else None,
    redoc_url="/redoc" if debug else None,
)

register_cors_middleware(app)

register_info_routes(app)
register_coctails_routes(app)
register_glasses_routes(app)
register_ingridients_routes(app)
register_file_storage_routes(app)
