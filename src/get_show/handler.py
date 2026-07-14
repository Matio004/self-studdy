import os
import boto3

from common.middleware import api
from common.services import Shows


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api
def lambda_handler(request, name):
    return 200, shows_service.get_show(name).model_dump(mode="json")
