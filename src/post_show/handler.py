from common.model import Show
import os
import boto3

from common.middleware import api
from common.services import Shows


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api(Show)
def lambda_handler(request):
    return 200, shows_service.put_show(request.body)
