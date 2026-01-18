INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "placed": {
            "type": "integer",
            "minimum": -2147483647,
            "maximum": 2147483647
        },
        "approved": {
            "type": "integer",
            "minimum": -2147483647,
            "maximum": 2147483647
        },
        "delivered": {
            "type": "integer",
            "minimum": -2147483647,
            "maximum": 2147483647
        }
    }
}