import urllib

from model import Seasons
from services import get_show, get_seasons
from utlis import render


def shows(event, context):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    return render(200, get_show(name).model_dump_json())

def seasons(event, context):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    return render(200, Seasons.dump_json(get_seasons(name)))