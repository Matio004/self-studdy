import os
import urllib

import boto3

from model import Episodes, Seasons
from services import Shows
from utlis import render

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


def shows(event, context):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    return render(200, shows_service.get_show(name).model_dump_json())


def seasons(event, context):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    return render(200, Seasons.dump_json(shows_service.get_seasons(name)))


def episodes(event, context):
    raw_name = event["pathParameters"]["name"]
    raw_season = event["pathParameters"]["season"]

    name = urllib.parse.unquote(raw_name).lower().strip()
    season = int(urllib.parse.unquote(raw_season).strip())

    return render(200, Episodes.dump_json(shows_service.get_episodes(name, season)))


def delete_show(event, content):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    shows_service.delete_show(name)
    return render(204, "")
