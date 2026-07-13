from exceptions import DomainException, RepositoryException, ExternalServiceException
from serializers import Response
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
                kwargs[name] = PARSERS[hint](path_params[name])
        request = None  # warn rite tequest

        try:
            response = fun(
                request, *args, **kwargs
            )  # todo write response model, validate, return str
        except DomainException as e:
            response = 404, {"message": str(e)}
        except RepositoryException as e:
            response = 500, {"message": str(e)}
        except ExternalServiceException as e:
            response = 404, {"message": str(e)}

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
