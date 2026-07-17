from . import logging
import requests
from .exceptions import TvMazeException
from .model import Episodes, Seasons, Show
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def get_show(name):
    response = requests.get(
        "https://api.tvmaze.com/singlesearch/shows", params={"q": name}
    )

    if response.ok:
        return Show.model_validate(response.json())

    try:
        response.raise_for_status()
    except HTTPError as e:
        logger.warning("Show not found")
        raise TvMazeException("Show not found") from e  # todo proper error handling


def get_seasons(id):
    response = requests.get(f"https://api.tvmaze.com/shows/{id}/seasons")

    if response.ok:
        return Seasons.validate_python(response.json())

    try:
        response.raise_for_status()
    except HTTPError as e:
        logger.warning("Season not found")
        raise TvMazeException("Season not found") from e  # todo proper error handling


def get_episodes(id):
    response = requests.get(f"https://api.tvmaze.com/seasons/{id}/episodes")

    if response.ok:
        return Episodes.validate_python(response.json())

    try:
        response.raise_for_status()
    except HTTPError as e:
        logger.warning("Epsiode not found")
        raise TvMazeException("Episode not found") from e  # todo proper error handling
