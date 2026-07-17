from . import logging
from boto3.dynamodb.conditions import Key
from .exceptions import NotFoundException, DomainException
from .repository import ShowRepository, SeasonRepository, EpisodeRepository

from . import api

logger = logging.getLogger(__name__)


class Shows:
    def __init__(self, table):
        self.table = table
        self.show_repository = ShowRepository(table)
        self.season_repository = SeasonRepository(table)
        self.episode_repository = EpisodeRepository(table)

    def get_show(self, name):
        try:
            show = self.show_repository.get_show(name)
            logger.info("Show %s retrived form repsitory", show.name)
            return show
        except NotFoundException:
            show = api.get_show(name)
            self.show_repository.put_show(show)
            logger.info("Show %s retrived form api and saved to repository", show.name)
            return show

    def get_seasons(self, name):
        try:
            show = self.get_show(name)
            seasons = self.season_repository.get_seasons(show.name)
            logger.info(
                "Total of %d seasons were found in repository for show %s",
                len(seasons),
                show.name,
            )
            return seasons
        except NotFoundException:
            seasons = api.get_seasons(show.id)
            self.season_repository.put_seasons(show.name, seasons)

            logger.info(
                "Total of %d seasons were found in api and saved for show %s",
                len(seasons),
                show.name,
            )
            return seasons

    def get_episodes(self, name, season):
        try:
            episodes = self.episode_repository.get_episodes(name, season)
            logger.info(
                "Total of %d episodes were found in repository for show %s in season %d",
                len(episodes),
                name,
                season,
            )
            return
        except NotFoundException:
            seasons = self.get_seasons(name)

            for s in seasons:
                if s.number == season:
                    episodes = api.get_episodes(s.id)

                    self.episode_repository.put_episodes(name, s.number, episodes)

                    logger.info(
                        "Total of %d episodes were found in api and saved for show %s in season %d",
                        len(episodes),
                        name,
                        season,
                    )
                    return episodes
        raise DomainException("Season number out of range for this show")

    def delete_show(self, name):
        response = self.table.query(
            KeyConditionExpression=Key("name").eq(name)
        )  # todo może zwrócić tylko część, użyć

        if not response["Items"]:
            raise NotFoundException("There is to show of such name.")

        with self.table.batch_writer() as batch:
            for item in response["Items"]:
                batch.delete_item(Key={"name": item["name"], "sk": item["sk"]})
        logger.info("Show, seasons and episodes were deleted for %s", name)
        return response["Items"]

    def put_show(self, show):
        logger.info("New show created, %s", show.name)
        return self.show_repository.put_show(show)

    def put_season(self, name, season):
        try:
            self.show_repository.get_show(name)
        except NotFoundException:
            logger.error("Attempted to create season for no existing show: %s", name)
            raise DomainException("You cant add season to non existing show")
        else:
            logger.info("Created season #%d for show: %s", season.number, name)
            return self.season_repository.put_season(name, season)

    def put_episode(self, name, season, episode):
        try:
            self.show_repository.get_show(name)
            self.season_repository.get_season(name, season)
        except NotFoundException:
            logger.error(
                "Attempted to create episode for non existing show/season: %s %d",
                name,
                season,
            )
            raise DomainException("You cant add episode to non existing show/season")
        else:
            logger.info(
                "Created episode %d for %s season#%d", episode.number, name, season
            )
            return self.episode_repository.put_episode(name, season, episode)
