from .available_values import cur, country
transaction_schema_post = {
    "type": "object",
    "properties": {
        "client_id": {"type": "number"},
        "cur": {
            "type": "string",
            "enum" : cur
            },
        "country": {
            "type": "string",
            "enum" : country
            },
        "date": {"type": "number"},
        "amount": {"type": "number"}
    },
    "required" : ["client_id", "cur", "country"],
    "additionalProperties": False
}
