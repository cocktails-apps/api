from fastapi import FastAPI

from ..storage import Storage


def get_storage(app: FastAPI) -> Storage:
    return app.state.storage  # type: ignore[no-any-return]
