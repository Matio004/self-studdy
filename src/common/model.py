from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class Country(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    code: str
    timezone: str

class Network(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    country: Country | None = None
    official_site: str | None = Field(alias='officialSite')


class Schedule(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    time: str
    days: list[str]


class Rating(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    average: Decimal | None = None


class Externals(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tvrage: int | None = None
    thetvdb: int | None = None
    imdb: str | None = None


class Image(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    medium: str | None = None
    original: str | None = None


class Link(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    href: str
    name: str | None = None

class Show(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    url: str
    name: str
    type: str
    language: str
    genres: list[str]
    status: str

    runtime: int | None = None
    average_runtime: int | None = Field(default=None, alias='averageRuntime')

    premiered: str | None = None
    ended: str | None = None

    official_site: str | None = Field(alias='officialSite')
    
    schedule: Schedule
    rating: Rating

    weight: int

    network: Network | None = None
    web_channel: Network | None = Field(default=None, alias='webChannel')
    dvd_country: Country | None = Field(default=None, alias='dvdCountry')

    externals: Externals
    image: Image | None = None

    summary: str | None = ''
    updated: int

    links: dict[str, Link] = Field(alias='_links')


class Season(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    url: str
    number: int
    name: str = ''
    episode_order: int = Field(alias='episodeOrder')
    premiere_date: str | None = Field(None, alias='premiereDate')
    end_date: str | None = Field(None, alias='endDate')
    network: Network | None = None
    web_channel: Network | None = Field(default=None, alias='webChannel')

    links: dict[str, Link] = Field(alias='_links')


Seasons = TypeAdapter(list[Season])


class Episode(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    url: str
    name: str | None = ''

    season: int
    number: int | None = 0  # todo if there are 2 specials it will breake 

    type: str

    airdate: str
    airtime: str
    airstamp: datetime

    runtime: int | None = None
    rating: Rating
    image: Image | None = None
    summary: str | None = ''

    links: dict[str, Link] = Field(alias='_links')
    

Episodes = TypeAdapter(list[Episode])