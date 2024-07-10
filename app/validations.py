import jsonschema
from jsonschema import validate

#Aquí se hacen validaciones básicas de los objetos tasks
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
    #Se usa el task_schema para validar los campos de prueba
    validate(instance=data, schema=task_schema)
