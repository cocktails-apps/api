import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

CORS_ORIGINS_ENV = "CORS_ORIGINS"


def register_cors_middleware(app: FastAPI) -> None:
    value = os.getenv(CORS_ORIGINS_ENV)
    if value is None:
        return

    origins = [origin.strip() for origin in value.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
