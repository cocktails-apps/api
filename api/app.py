from fastapi import FastAPI

from .routes import (
    register_coctails_routes,
    register_file_storage_routes,
    register_glasses_routes,
    register_info_routes,
    register_ingridients_routes,
)

app = FastAPI()
register_info_routes(app)
register_coctails_routes(app)
register_glasses_routes(app)
register_ingridients_routes(app)
register_file_storage_routes(app)
