from fastapi import FastAPI

from .routes import register_info_routes

app = FastAPI()

register_info_routes(app)
