from datetime import datetime, timezone

SCHEMA = {
    "name": "get_current_time",
    "description": "Return the current date and time in UTC.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

OPENAI_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": SCHEMA["description"],
        "parameters": SCHEMA["input_schema"],
    },
}


def run(input: dict) -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")
