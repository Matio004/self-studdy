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
                kwargs[name] = PARSERS[hint](path_params[name])
        request = None  # warn rite tequest
        response = fun(
            request, *args, **kwargs
        )  # todo write response model, validate, return str

        return {
            "statusCode": response[0],
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(response[1]),
        }

    return wrapper
