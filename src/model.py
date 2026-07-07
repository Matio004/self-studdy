from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, TypeAdapter


class Country(BaseModel):
    name: str
    code: str
    timezone: str

class Network(BaseModel):
    id: int
    name: str
    country: Country | None = None
    official_site: str | None = Field(alias='officialSite')


class Schedule(BaseModel):
    time: str
    days: list[str]


class Rating(BaseModel):
    average: Decimal | None = None


class Externals(BaseModel):
    tvrage: int | None = None
    thetvdb: int | None = None
    imdb: str | None = None


class Image(BaseModel):
    medium: str | None = None
    original: str | None = None


class Link(BaseModel):
    href: str
    name: str | None = None

class Show(BaseModel):
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
    id: int
    url: str
    number: int
    name: str = ''
    episode_order: int = Field(alias='episodeOrder')
    premiere_date: str = Field(alias='premiereDate')
    end_date: str = Field(alias='endDate')
    network: Network | None = None
    web_channel: Network | None = Field(default=None, alias='webChannel')

    links: dict[str, Link] = Field(alias='_links')


Seasons = TypeAdapter(list[Season])


class Episode(BaseModel):
    id: int
    url: str
    name: str | None = ''

    season: int
    number: int

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