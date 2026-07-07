from pydantic import BaseModel


def render(status, body: BaseModel):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body.model_dump_json()
    }