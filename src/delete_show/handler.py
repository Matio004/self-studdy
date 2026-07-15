from common.serializers import ShowNamePathParam
import os
from common.services import Shows
import boto3
from common.middleware import api

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

shows_service = Shows(table)


@api(path_param=ShowNamePathParam)
def lambda_handler(request, name):
    shows_service.delete_show(name)
    return 204, {}
