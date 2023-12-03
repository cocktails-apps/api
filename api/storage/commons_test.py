from .commons import ApiBaseModel


def test_api_base_model_json():
    class Model(ApiBaseModel):
        some_value: str

    m = Model(some_value="test")

    doc = m.model_dump(by_alias=True)
    assert doc == {"someValue": "test"}
