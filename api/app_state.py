from typing import TypedDict

from .storage import Storage


class AppState(TypedDict):
    storage: Storage
