from common.serializers import GetEpisodesPathParams
from common.model import Episode
import os
import boto3

from common.middleware import api
from common.services import Shows


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api(Episode, GetEpisodesPathParams)
def lambda_handler(request, name, season: int):
    return 200, shows_service.put_episode(name, season, request.body)
