from datetime import date, datetime

from pydantic import BaseModel, Field, HttpUrl


class Country(BaseModel):
    name: str
    code: str
    timezone: str

class Network(BaseModel):
    id: int
    name: str
    country: Country | None
    official_site: HttpUrl | None = Field(alias='officialSite')


class Schedule(BaseModel):
    time: str
    days: list[str]


class Rating(BaseModel):
    average: float | None


class Externals(BaseModel):
    tvrage: int | None
    thetvdb: int | None
    imdb: str | None


class Image(BaseModel):
    medium: HttpUrl | None
    original: HttpUrl | None


class Link(BaseModel):
    href: HttpUrl
    name: str | None

class Show(BaseModel):
    id: int
    url: HttpUrl
    name: str
    type: str
    language: str
    genres: list[str]
    status: str

    runtime: int | None = None
    average_runtime: int | None = Field(default=None, alias='averageRuntime')

    premiered: date | None = None
    ended: date | None = None

    official_site: HttpUrl | None = Field(alias='officialSite')
    
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
    url: HttpUrl
    number: int
    name: str = ''
    episode_order = int = Field(alias='episodeOrder')
    premiere_date = date = Field(alias='premiereDate')
    end_date = date = Field(alias='endDate')
    network = Network | None = None
    web_channel: Network | None = Field(default=None, alias='webChannel')

    links: dict[str, Link] = Field(alias='_links')


class Episode(BaseModel):
    id: int
    url: HttpUrl
    name: str | None = ''

    season: int
    number: int

    type: str

    airdate: date
    airtime: str
    airstamp: datetime

    runtime: int | None = None
    rating: Rating
    image: Image | None = None
    summary: str | None = ''

    links: dict[str, Link] = Field(alias='_links')
    