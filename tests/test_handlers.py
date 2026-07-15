from unittest.mock import patch
from moto import mock_aws
from get_show.handler import lambda_handler as get_show_handler


@patch("os.environ", {"TABLE_NAME": "services_by_name"})
def test_get_show_handler(show):
    response = get_show_handler({"pathParameters": {"name": show.name}}, None)
    # todo
