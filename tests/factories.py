import random

import factory
import model


class CountryFactory(factory.Factory):
    class Meta:
        model = model.Country

    name = factory.Faker("country")
    code = factory.Faker("country_code")
    timezone = factory.Faker("timezone")


class NetworkFactory(factory.Factory):
    class Meta:
        model = model.Network

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("company")
    country = factory.SubFactory(CountryFactory)
    official_site = factory.Faker("url")


class ScheduleFactory(factory.Factory):
    class Meta:
        model = model.Schedule

    time = factory.Faker("time")
    days = factory.LazyFunction(
        lambda: random.sample(
            ["monday", "tuesday", "wednesday", "thursday", "friday"],
            k=2,
        )
    )


class RatingFactory(factory.Factory):
    class Meta:
        model = model.Rating

    average = factory.Faker("pyfloat")


class ExternalsFactory(factory.Factory):
    class Meta:
        model = model.Externals

    tvrage = factory.Faker("random_int", min=1, max=999999)
    thetvdb = factory.Faker("random_int", min=1, max=999999)
    imdb = factory.Faker("bothify", text="tt########")


class ImageFactory(factory.Factory):
    class Meta:
        model = model.Image

    medium = factory.Faker("url")
    original = factory.Faker("url")


class LinkFactory(factory.Factory):
    class Meta:
        model = model.Link

    href = factory.Faker("url")
    name = factory.Faker("word")


class ShowFactory(factory.Factory):
    class Meta:
        model = model.Show

    id = factory.Sequence(lambda n: n + 1)
    url = factory.Faker("url")
    name = factory.Faker("catch_phrase")
    type = factory.Faker("word")
    language = factory.Faker("word")
    genres = factory.Faker("words")
    status = factory.Faker("word")

    runtime = factory.Faker("random_int", min=1, max=999999)
    average_runtime = factory.Faker("random_int", min=1, max=999999)

    premiered = factory.Faker("date")
    ended = factory.Faker("date")

    official_site = factory.Faker("url")

    schedule = factory.SubFactory(ScheduleFactory)
    rating = factory.SubFactory(RatingFactory)

    weight = factory.Faker("random_int", min=1, max=200)

    network = factory.SubFactory(NetworkFactory)
    web_channel = factory.SubFactory(NetworkFactory)
    dvd_country = factory.SubFactory(CountryFactory)

    externals = factory.SubFactory(ExternalsFactory)
    image = factory.SubFactory(ImageFactory)

    summary = factory.Faker("paragraph")
    updated = factory.Faker("random_int", min=0, max=9999)

    links = {}


class SeasonFactory(factory.Factory):
    class Meta:
        model = model.Season

    id = factory.Sequence(lambda n: n + 1)
    url = factory.Faker("url")
    number = factory.Faker("random_int", min=1, max=20)
    name = factory.Faker("catch_phrase")

    episode_order = factory.Faker(
        "random_int",
        min=1,
        max=30,
    )

    premiere_date = factory.Faker(
        "date",
        pattern="%Y-%m-%d",
    )

    end_date = factory.Faker(
        "date",
        pattern="%Y-%m-%d",
    )

    network = factory.SubFactory(NetworkFactory)
    web_channel = factory.SubFactory(NetworkFactory)

    links = factory.LazyFunction(
        lambda: {
            "self": LinkFactory(),
            "previousepisode": LinkFactory(),
            "nextepisode": LinkFactory(),
        }
    )


class EpisodeFactory(factory.Factory):
    class Meta:
        model = model.Episode

    id = factory.Sequence(lambda n: n + 1)
    url = factory.Faker("url")
    name = factory.Faker("catch_phrase")

    season = factory.Faker("random_int", min=1, max=20)
    number = factory.Faker("random_int", min=1, max=20)

    type = factory.Faker("word")

    rating = factory.SubFactory(RatingFactory)
    image = factory.SubFactory(ImageFactory)

    summary = factory.Faker("paragraph")

    links = factory.LazyFunction(
        lambda: {
            "self": LinkFactory(),
            "previousepisode": LinkFactory(),
            "nextepisode": LinkFactory(),
        }
    )
