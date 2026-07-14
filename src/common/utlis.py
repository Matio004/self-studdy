from pydantic import BaseModel


def render(status, body: str):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }