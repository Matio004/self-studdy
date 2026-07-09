from boto3.dynamodb.conditions import Key

import api
from model import Episodes, Show, Seasons


class Shows:
    def __init__(self, table):
        self.table = table

    def get_show(self, name):
        item = self.table.get_item(Key={"name": name, "sk": "SHOW"})

        if "Item" in item:
            return Show.model_validate(item["Item"]["data"])

        show = api.get_show(name)

        self.table.put_item(
            Item={"name": show.name, "sk": "SHOW", "data": show.model_dump(mode="json")}
        )

        return show

    def get_seasons(self, name):
        show = self.get_show(name)

        response = self.table.query(
            KeyConditionExpression=Key("name").eq(show.name)
            & Key("sk").begins_with("SEASON#")
        )

        if response["Items"]:
            return Seasons.validate_python([item["data"] for item in response["Items"]])

        seasons = api.get_seasons(show.id)

        with self.table.batch_writer() as batch:
            for season in seasons:
                batch.put_item(
                    Item={
                        "name": show.name,
                        "sk": f"SEASON#{season.number}",
                        "data": season.model_dump(mode="json"),
                    }
                )

        return seasons

    def get_episodes(self, name, season):
        seasons = self.get_seasons(name)

        response = self.table.query(
            KeyConditionExpression=Key("name").eq(name)
            & Key("sk").begins_with(f"EPISODE#{season}#")
        )

        if response["Items"]:
            return Episodes.validate_python(
                [item["data"] for item in response["Items"]]
            )

        for s in seasons:
            if s.number == season:
                episodes = api.get_episodes(s.id)

                with self.table.batch_writer() as batch:
                    for episode in episodes:
                        batch.put_item(
                            Item={
                                "name": name,
                                "sk": f"EPISODE#{s.number}#{episode.number}",
                                "data": episode.model_dump(mode="json"),
                            }
                        )
                return episodes
        raise ValueError("Season number out of range for this show")

    def delete_show(self, name):
        response = self.table.query(
            Key={
                "name": name,
            }
        )  # todo może zwrócić tylko część, użyć

        if "Item" not in response:
            raise KeyError("There is to show of such name.")

        with self.table.batch_writer() as batch:
            for item in response["Items"]:
                batch.delete_item(Key={"name": item["name"], "sk": item["sk"]})
        return response["Items"]
