INVENTORY_SCHEMA = {
    "type": "object",
    "additionalProperties": {
        "type": "integer",
        "minimum": -2147483647,   # int32 min
        "maximum": 2147483647     # int32 max
    }
}