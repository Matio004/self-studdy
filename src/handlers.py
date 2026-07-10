from middleware import api
import os

import boto3

from model import Episodes, Seasons
from services import Shows

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api
def shows(request, name):
    return 200, shows_service.get_show(name).model_dump(mode="json")


@api
def seasons(request, name):
    return 200, Seasons.dump_python(shows_service.get_seasons(name), mode="json")


@api
def episodes(request, name, season: int):
    return 200, Episodes.dump_python(
        shows_service.get_episodes(name, season), mode="json"
    )


@api
def delete_show(request, name):
    # shows_service.delete_show(name)
    return 204, {}
