import os
import boto3

from common.middleware import api
from common.model import Episodes
from common.services import Shows

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api
def lambda_handler(request, name, season: int):
    return 200, Episodes.dump_python(
        shows_service.get_episodes(name, season), mode="json"
    )
