import pytest

from conftest import dynamodb_table, show, seasons
from common.services import Shows


def test_get_show(dynamodb_table, show):
    shows = Shows(dynamodb_table)

    assert shows.get_show(show.name).id == show.id


def test_get_seasons(dynamodb_table, show, seasons):
    pass


def test_get_episodes(dynamodb_table, show):
    pass


def test_delete_show(dynamodb_table, show):
    pass
