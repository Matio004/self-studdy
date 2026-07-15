from common.serializers import ShowNamePathParam
import os
import boto3

from common.middleware import api
from common.services import Shows


def get_service():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])

    return Shows(table)


@api(path_param=ShowNamePathParam)
def lambda_handler(request, name):
    return 200, get_service().get_show(name).model_dump(mode="json")


# TODO post, db sindex,
