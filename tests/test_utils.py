import api
from utlis import render

def test_render():
    show = api.get_show('house')

    response = render(200, show)

    assert response['statusCode'] == 200
    assert response['body']['name'] == 'House'