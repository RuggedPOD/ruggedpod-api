import json

from ruggedpod_api.common import exception


def parse_json_body(request):
    if not request.data:
        return {}
    try:
        return json.loads(request.data)
    except ValueError:
        raise exception.BodySyntaxError()
