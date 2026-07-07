import os

import boto3

import api
from model import Show

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['TABLE_NAME'])


def get_show(name):
    item = table.get_item(
        Key={
            "name": name
        }
    )

    if "Item" in item:
        return Show.model_validate(item["Item"])
    
    show = api.get_show(name)

    table.put_item(
        Item={
            "name": show.name,
            "data": show.model_dump(mode='json')
        }
    )

    return show

def get_seasons(name):
    show = get_show(name)

    return api.get_seasons(show.id)

def get_episodes(name, season):
    seasons = get_seasons(name)

    for s in seasons:
        if s.number == season:
            return api.get_episodes(season.id)
    raise ValueError('Season number out of range for this show')