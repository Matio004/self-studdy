import pytest

from common.model import Show
from common.serializers import create_request_model


def test_create_req_model():
    req_model = create_request_model(body=Show)

    assert req_model.model_fields["body"].annotation is Show
    assert req_model.__name__ == "RequestShow"
