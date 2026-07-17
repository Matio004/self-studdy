from common.exceptions import NotFoundException
from common.repository import EpisodeRepository
import pytest

from .factories import ShowFactory, SeasonFactory, EpisodeFactory


def test_show_repository(show_repo):
    with pytest.raises(NotFoundException):
        show_repo.get_show("name")

    show = ShowFactory.build()
    show_repo.put_show(show)

    assert show_repo.get_show(show.name).name == show.name


def test_season_repository(season_repo, show):
    with pytest.raises(NotFoundException):
        season_repo.get_seasons("name")

    seasons = [SeasonFactory.build(), SeasonFactory.build()]

    season_repo.put_seasons(show.name, seasons)

    assert season_repo.get_seasons(show.name)
    assert len(season_repo.get_seasons(show.name)) == len(seasons)


def test_episode_repository(episode_repo, show, seasons):
    with pytest.raises(NotFoundException):
        episode_repo.get_episodes("name", 1)

    episodes = [EpisodeFactory.build(), EpisodeFactory.build()]

    episode_repo.put_episodes(show.name, seasons[0].number, episodes)

    assert episode_repo.get_episodes(show.name, seasons[0].number)
    assert len(episode_repo.get_episodes(show.name, seasons[0].number)) == len(episodes)
