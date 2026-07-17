from . import logging
from .exceptions import NotFoundException
from .model import Show, Seasons, Episodes, Episode, Season
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)


class ShowRepository:
    def __init__(self, table):
        self.table = table

    def get_show(self, name):
        item = self.table.get_item(Key={"name": name, "sk": "SHOW"})
        if "Item" in item:
            logger.debug("Show %s found in bd", name)
            return Show.model_validate(item["Item"]["data"])
        logger.debug("Show %s not found db", name)
        raise NotFoundException("Show not found")

    def put_show(self, show):
        response = self.table.put_item(
            Item={
                "name": show.name,
                "sk": "SHOW",
                "data": show.model_dump(mode="json"),
            },
        )  # TODO return added item
        logger.debug("Show created: %s", show.name)

    def delete_show(self, name):
        pass


class SeasonRepository:
    def __init__(self, table):
        self.table = table

    def get_season(self, name, number):
        item = self.table.get_item(Key={"name": name, "sk": f"SEASON#{number}"})

        if "Item" in item:
            logger.debug("Season %d for show %s found in db", number, name)
            return Season.model_validate(item["Item"]["data"])
        logger.debug("Season %d for show %s not found in db", number, name)
        raise NotFoundException("Season not found")

    def get_seasons(self, name):
        response = self.table.query(
            KeyConditionExpression=Key("name").eq(name)
            & Key("sk").begins_with("SEASON#")
        )

        if response["Items"]:
            logger.debug("Seasons for show %s found in db", name)
            return Seasons.validate_python([item["data"] for item in response["Items"]])
        logger.debug("Seasons for show %s not found in db", name)
        raise NotFoundException("Show`s seasons not found")

    def put_season(self, name, season):
        response = self.table.put_item(
            Item={
                "name": name,
                "sk": f"SEASON#{season.number}",
                "data": season.model_dump(mode="json"),
            },
        )
        logger.debug("Season %d for show %s created", season.number, name)

    def put_seasons(self, name, seasons):
        with self.table.batch_writer() as batch:
            for season in seasons:
                batch.put_item(
                    Item={
                        "name": name,
                        "sk": f"SEASON#{season.number}",
                        "data": season.model_dump(mode="json"),
                    }
                )
        logger.debug("Seasons for show %s created", name)


class EpisodeRepository:
    def __init__(self, table):
        self.table = table

    def get_episodes(self, name, season):
        response = self.table.query(
            KeyConditionExpression=Key("name").eq(name)
            & Key("sk").begins_with(f"EPISODE#{season}#")
        )
        if response["Items"]:
            logger.debug("Episode for show %s for season %d found in db", name, season)
            return Episodes.validate_python(
                [item["data"] for item in response["Items"]]
            )
        logger.debug("Episode for show %s for season %d not found in db", name, season)
        raise NotFoundException("Seasons' episodes not found")

    def put_episode(self, name, season, episode):
        response = self.table.put_item(
            Item={
                "name": name,
                "sk": f"EPISODE#{season}#{episode.number}",
                "data": episode.model_dump(mode="json"),
            },
        )
        logger.debug(
            "Epiode %d in season #%d for show %s created", episode.number, season, name
        )

    def put_episodes(self, name, season, episodes):
        with self.table.batch_writer() as batch:
            for episode in episodes:
                batch.put_item(
                    Item={
                        "name": name,
                        "sk": f"EPISODE#{season}#{episode.number}",
                        "data": episode.model_dump(mode="json"),
                    }
                )
        logger.debug("Epiodes in season #%d for show %s created", season, name)
