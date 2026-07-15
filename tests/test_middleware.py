import json
from common.middleware import api
from common.model import Show
import pytest
from factories import ShowFactory


def test_api_middleware():
    fun = api(Show)
    wrapped = fun(lambda x: (200, x.body.model_dump(mode="json")))

    response = wrapped({"body": Show.model_dump(ShowFactory.build(), mode="json")}, {})
