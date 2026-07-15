from common.serializers import ShowNamePathParam
from common.model import Season
import os
import boto3

from common.middleware import api
from common.services import Shows


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api(Season, ShowNamePathParam)
def lambda_handler(request, name):
    return 200, shows_service.put_season(name, request.body)
