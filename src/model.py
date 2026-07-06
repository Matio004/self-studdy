from datetime import date
from typing import Optional
from urllib import HttpUrl

from pydantic import BaseModel, Field


class Country(BaseModel):
    name: str
    code: str
    timezone: str

class Network(BaseModel):
    id: int
    name: str
    country: Country | None
    officialSite: HttpUrl | None


class Schedule(BaseModel):
    time: str
    days: list[str]


class Rating(BaseModel):
    average: float | None


class Externals(BaseModel):
    tvrage: int | None
    thetvdb: int | None
    imdb: str


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
    languages: str
    genres: list[str]
    status: str

    runtime: int
    averageRuntime: int

    premiered: date | None
    ended: date | None

    officialSite: HttpUrl | None
    
    schedule: Schedule
    rating: Rating

    weight: int

    network: Network | None
    webChannel: Network | None
    dvdCountry: Country | None

    externals: Externals
    image: Image | None

    summary: str = Field(default='')
    updated: int

    links: dict[str, Link] = Field(alias='_links')
