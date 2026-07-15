from pydantic import BaseModel, ConfigDict, Field, create_model


class Request(BaseModel):
    path_params: BaseModel | None
    query_params: BaseModel | None

    body: BaseModel | None


class Response(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status_code: int = Field(alias="statusCode")
    headers: dict[str, str]
    body: str


class ShowNamePathParam(BaseModel):
    name: str


class GetEpisodesPathParams(BaseModel):
    name: str
    season: int


def create_request_model(**kwargs):
    new_fields = {}
    model_name = Request.__name__

    for f_name in Request.model_fields.keys():
        annot = kwargs.get(f_name)
        new_fields[f_name] = annot

        if annot:
            model_name += annot.__name__
    return create_model(model_name, __base__=Request, **new_fields)  # innore
