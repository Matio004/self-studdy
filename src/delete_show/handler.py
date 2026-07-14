from common.middleware import api


@api
def lambda_handler(request):
    return 200, {"message": "OK"}
