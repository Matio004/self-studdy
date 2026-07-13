from exceptions import TvMazeException
import pytest
from logging import getLogger

from api import get_episodes, get_show, get_seasons

logger = getLogger(__name__)


def test_show():
    show = get_show("house")

    assert show.name == "House"

    with pytest.raises(TvMazeException):
        get_show("1231231321331231231")


def test_seasons():
    seasons = get_seasons(118)

    assert seasons
    assert seasons[0].number == 1


def test_episodes():
    episodes = get_episodes(554)

    assert episodes
    assert episodes[0].number == 1
