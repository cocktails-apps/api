from datetime import datetime
from typing import Annotated, Any

import humps
from bson import Timestamp
from pydantic import BaseModel, ConfigDict
from pydantic.types import StringConstraints


class ApiBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=humps.camelize,
        populate_by_name=True,
        frozen=True,
    )


Name = Annotated[
    str, StringConstraints(to_lower=True, strip_whitespace=True, min_length=1)
]
Description = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def add_metadata(doc: dict[str, Any]) -> dict[str, Any]:
    doc["metadata"] = dict(
        createdAt=Timestamp(datetime.utcnow(), 0),
    )
    return doc


class DocumentNotFound(ValueError):
    pass
