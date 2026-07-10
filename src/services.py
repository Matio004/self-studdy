from repository import ShowRepository, SeasonRepository, EpisodeRepository

import api


class Shows:
    def __init__(self, table):
        self.show_repository = ShowRepository(table)
        self.season_repository = SeasonRepository(table)
        self.episode_repository = EpisodeRepository(table)

    def get_show(self, name):
        try:
            return self.show_repository.get_show(name)
        except KeyError:
            show = api.get_show(name)
            self.show_repository.put_show(show)
            return show

    def get_seasons(self, name):
        try:
            show = self.get_show(name)
            return self.season_repository.get_seasons(show.name)
        except KeyError:
            seasons = api.get_seasons(show.id)
            self.season_repository.put_seasons(show.name, seasons)

            return seasons

    def get_episodes(self, name, season):
        try:
            return self.episode_repository.get_episodes(name, season)
        except KeyError:
            seasons = self.get_seasons(name)

            for s in seasons:
                if s.number == season:
                    episodes = api.get_episodes(s.id)

                    self.episode_repository.put_episodes(name, s.number, episodes)

                    return episodes
        raise ValueError("Season number out of range for this show")

    """def delete_show(self, name):
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
        return response["Items"]"""
