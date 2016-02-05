import json

from ruggedpod_api.common import exception


def parse_json_body(request):
    try:
        return json.loads(request.data)
    except ValueError:
        raise exception.BodySyntaxError()
