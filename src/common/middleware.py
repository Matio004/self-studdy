from .exceptions import AppException, DomainException

from .serializers import Response
import json
import urllib.parse
import inspect
from typing import get_type_hints


PARSERS = {
    int: lambda x: int(x.strip()),
    str: lambda x: urllib.parse.unquote(x).strip(),
}


def api(fun):
    sig = inspect.signature(fun)
    hints = get_type_hints(fun)

    def wrapper(event, context, *args, **kwargs):

        try:
            path_params = event.get("pathParameters", {})
            kwargs = {}

            for name in sig.parameters:
                if "request".startswith(name):
                    continue
                if name in path_params:
                    hint = hints.get(name, str)

                    if hint not in PARSERS:
                        raise TypeError("Unknown type for path parameter")
                    # TODO handle parsing exceptions
                    try:
                        kwargs[name] = PARSERS[hint](path_params[name])
                    except ValueError:
                        raise DomainException(f"{name} should be {hint}")
            request = None  # warn rite tequest

            response = fun(
                request, *args, **kwargs
            )  # todo write response model, validate, return str
        except AppException as e:
            response = e.status_code, {"message": str(e)}

        return Response.model_validate(
            {
                "statusCode": response[0],
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": json.dumps(response[1]),
            }
        ).model_dump(by_alias=True)

    return wrapper
