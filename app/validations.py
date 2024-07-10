import jsonschema
from jsonschema import validate

task_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "completed": {"type": "boolean"},
    },
    "required": ["title", "description"],
    "additionalProperties": False
}

def validate_task(data):
    validate(instance=data, schema=task_schema)
