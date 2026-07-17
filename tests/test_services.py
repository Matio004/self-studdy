from common.exceptions import NotFoundException
from unittest.mock import patch
import pytest

from common.services import Shows
from .factories import ShowFactory, SeasonFactory, EpisodeFactory


@patch("common.api.get_show")
def test_get_show(mock_get_show, dynamodb_table, show):
    mock_get_show.side_effect = lambda x: ShowFactory.build(name=x)
    shows = Shows(dynamodb_table)

    assert shows.get_show(show.name).id == show.id
    assert shows.get_show("name")

    mock_get_show.assert_called_once()


@patch("common.services.Shows.get_show")
@patch("common.api.get_seasons")
def test_get_seasons(
    mock_get_seasons,
    mock_get_show,
    dynamodb_table,
    show,
    seasons,
):
    mock_get_show.side_effect = lambda name: ShowFactory.build(name=name)
    mock_get_seasons.return_value = [SeasonFactory.build(id=-1)]

    shows = Shows(dynamodb_table)

    result = shows.get_seasons("name1")

    assert result[-1].id == -1

    mock_get_show.assert_called_once()
    mock_get_seasons.assert_called_once()


def test_get_episodes(dynamodb_table, show):
    pass


def test_delete_show(dynamodb_table, show, show_repo):
    shows = Shows(dynamodb_table)
    shows.delete_show(show.name)

    with pytest.raises(NotFoundException):
        show_repo.get_show(show.name)
