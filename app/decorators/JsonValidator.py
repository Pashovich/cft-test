import json
import jsonschema
from jsonschema import validate
from aiohttp.web import json_response
from jsonschema.exceptions import ValidationError


class JsonValidator(object):

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, func):
        async def _wrapper(obj, req):
            try:
                validate(instance=await req.json(), schema=self.schema)
            except ValidationError as e:
                return json_response({"error_msg" : e.message},status=422)
            return await func(obj, req)
        return _wrapper