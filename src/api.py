from exceptions import TvMazeException
import requests

from model import Episodes, Show, Seasons


def get_show(name):
    response = requests.get(
        "https://api.tvmaze.com/singlesearch/shows", params={"q": name}
    )

    if response.ok:
        return Show.model_validate(response.json())

    raise TvMazeException() from response.raise_for_status()  # todo proper error handling


def get_seasons(id):
    response = requests.get(f"https://api.tvmaze.com/shows/{id}/seasons")

    if response.ok:
        return Seasons.validate_python(response.json())

    raise TvMazeException() from response.raise_for_status()  # todo proper error handling


def get_episodes(id):
    response = requests.get(f"https://api.tvmaze.com/seasons/{id}/episodes")

    if response.ok:
        return Episodes.validate_python(response.json())

    raise TvMazeException() from response.raise_for_status()  # todo proper error handling

