import pytest

from factories import ShowFactory, SeasonFactory


def test_show_repository(show_repo):
    with pytest.raises(KeyError):
        show_repo.get_show("name")

    show = ShowFactory.build()
    show_repo.put_show(show)

    assert show_repo.get_show(show.name).name == show.name


def test_season_repository(season_repo):
    with pytest.raises(KeyError):
        season_repo.get_seasons("name")

    seasons = [SeasonFactory.build(), SeasonFactory.build()]
