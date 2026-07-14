from common import api
from common.utlis import render


def test_render():
    show = api.get_show("house")

    response = render(200, show.model_dump_json())

    assert response["statusCode"] == 200
    assert isinstance(response["body"], str)

