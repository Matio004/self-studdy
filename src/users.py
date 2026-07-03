import json

def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps([
            {"id": 1, "name": "Jan"}
        ])
    }