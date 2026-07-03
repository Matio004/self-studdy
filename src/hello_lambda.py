import json
import os
import requests
import boto3
import urllib

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['TABLE_NAME'])

def render(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    raw_name = event["pathParameters"]["name"]
    name = urllib.parse.unquote(raw_name).lower().strip()

    item = table.get_item(
        Key={
            "name": name
        }
    )

    
    if "Item" in item:
        return render(200, {
            "source": "dynamobd",
            "data": item["Item"]['name']
        })

    response = requests.get(
    "https://api.tvmaze.com/singlesearch/shows",
    params={"q": name},
    )
    response.raise_for_status()
    
    table.put_item(
        Item={
            "name": name,
            "data": json.dumps(response.json()["name"])
        }
    )


    return render(200, {
            "source": "api",
            "data": response.json()["name"]
        })
