import urllib

from model import Episodes, Seasons
from services import get_show, get_seasons, get_episodes
from utlis import render


def shows(event, context):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    return render(200, get_show(name).model_dump_json())

def seasons(event, context):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    return render(200, Seasons.dump_json(get_seasons(name)))

def episodes(event, context):
    raw_name = event["pathParameters"]["name"]
    raw_season = event["pathParameters"]["season"]

    name = urllib.parse.unquote(raw_name).lower().strip()
    season = int(urllib.parse.unquote(raw_season).strip())

    return render(200, Episodes.dump_json(get_episodes(name, season)))