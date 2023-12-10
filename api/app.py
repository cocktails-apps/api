import os

from fastapi import FastAPI

from .log import configure_logger
from .routes import (
    register_coctails_routes,
    register_file_storage_routes,
    register_glasses_routes,
    register_info_routes,
    register_ingridients_routes,
)

debug = os.environ.get("DEBUG", "false").lower() == "true"
configure_logger(debug)

app = FastAPI(debug=debug)
register_info_routes(app)
register_coctails_routes(app)
register_glasses_routes(app)
register_ingridients_routes(app)
register_file_storage_routes(app)
