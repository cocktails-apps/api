from datetime import datetime
from typing import Any

import humps
from bson import Timestamp
from pydantic import BaseModel, ConfigDict


class ApiBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=humps.camelize,
        populate_by_name=True,
        frozen=True,
    )


def add_metadata(doc: dict[str, Any]) -> dict[str, Any]:
    doc["metadata"] = dict(
        createdAt=Timestamp(datetime.utcnow(), 0),
    )
    return doc


class DocumentNotFound(ValueError):
    pass
