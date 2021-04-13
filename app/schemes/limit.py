from .available_values import cur, country
from copy import deepcopy
limit_schema_put = {
    "type": "object",
    "properties": {
        "cur": {
            "type": "string",
            "enum" : cur
            },
        "country": {
            "type": "string",
            "enum" : country
            },
        "limit": {"type": "number"}
    }
}

limit_schema_post = deepcopy(limit_schema_put)

limit_schema_post['required'] = ["cur", "country", "limit"]