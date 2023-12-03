from .commons import ApiBaseModel, Description, Name


def test_api_base_model_json() -> None:
    class Model(ApiBaseModel):
        some_value: str

    m = Model(some_value="test")

    doc = m.model_dump(by_alias=True)
    assert doc == {"someValue": "test"}


def test_name() -> None:
    class Model(ApiBaseModel):
        name: Name

    m = Model(name=" Test ")
    assert m.name == "test"


def test_description() -> None:
    class Model(ApiBaseModel):
        description: Description

    m = Model(description=" Some description ")
    assert m.description == "Some description"
