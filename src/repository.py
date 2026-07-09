from model import Show, Seasons, Episodes
from boto3.dynamodb.conditions import Key


class ShowRepository:
    def __init__(self, table):
        self.table = table

    def get_show(self, name):
        item = self.table.get_item(Key={"name": name, "sk": "SHOW"})
        if "Item" in item:
            return Show.model_validate(item["Item"]["data"])
        raise KeyError("Show not found")

    def put_show(self, show):
        self.table.put_item(
            Item={"name": show.name, "sk": "SHOW", "data": show.model_dump(mode="json")}
        )

    def delete_show(self, name):
        pass


class SeasonRepository:
    def __init__(self, table):
        self.table = table

    def get_seasons(self, name):
        response = self.table.query(
            KeyConditionExpression=Key("name").eq(name)
            & Key("sk").begins_with("SEASON#")
        )

        if response["Items"]:
            return Seasons.validate_python([item["data"] for item in response["Items"]])
        raise KeyError("Show`s seasons not found")

    def put_seasons(self, show, seasons):
        with self.table.batch_writer() as batch:
            for season in seasons:
                batch.put_item(
                    Item={
                        "name": show.name,
                        "sk": f"SEASON#{season.number}",
                        "data": season.model_dump(mode="json"),
                    }
                )


class EpisodeRepository:
    def __init__(self, table):
        self.table = table

    def get_episodes(self, name, season):
        response = self.table.query(
            KeyConditionExpression=Key("name").eq(name)
            & Key("sk").begins_with(f"value=EPISODE#{season}#")
        )
        if response["Items"]:
            return Episodes.validate_python(
                [item["data"] for item in response["Items"]]
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
