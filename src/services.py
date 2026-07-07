import os

import boto3
from boto3.dynamodb.conditions import Key

import api
from model import Episodes, Show, Seasons

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['TABLE_NAME'])


def get_show(name):
    item = table.get_item(
        Key={
            "name": name,
            "sk": "SHOW"
        }
    )

    if "Item" in item:
        return Show.model_validate(item["Item"])
    
    show = api.get_show(name)

    table.put_item(
        Item={
            "name": show.name,
            "sk": "SHOW",
            "data": show.model_dump(mode='json')
        }
    )

    return show

def get_seasons(name):
    show = get_show(name)

    response = table.query(
        KeyConditionExpression=Key('name').eq(show.name) & Key('sk').begins_with('SEASON#')
    )

    if response['Items']:
        return Seasons.validate_python([item['data'] for item in response["Items"]])
    
    seasons = api.get_seasons(show.id)
    
    with table.batch_writer() as batch:
        for season in seasons:
            batch.put_item(
                Item={
                    'name': show.name,
                    'sk': f'SEASON#{season.number}',
                    'data': season.model_dump(mode='json')
                }
            )

    return seasons

def get_episodes(name, season):
    seasons = get_seasons(name)

    response = table.query(
        KeyConditionExpression=Key('name').eq(name) & Key('sk').begins_with(f'EPISODE#{season}#')
    )
    
    if response['Items']:
        return Episodes.validate_python([item['data'] for item in response['Items']])
    

    for s in seasons:
        if s.number == season:
            episodes = api.get_episodes(s.id)

            with table.batch_writer() as batch:
                for episode in episodes:
                    batch.put_item(
                        Item={
                            'name': name,
                            'sk': f'EPISODE#{s.number}#{episode.number}',
                            'data': episode.model_dump(mode='json')
                        }
                    )
            return episodes
    raise ValueError('Season number out of range for this show')