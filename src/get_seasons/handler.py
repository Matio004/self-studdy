import os
import boto3

from common.middleware import api
from common.model import Seasons
from common.services import Shows

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api
def lambda_handler(request, name):
    return 200, Seasons.dump_python(shows_service.get_seasons(name), mode="json")
