from typing import Any
class AdvancedValidator:
    def validate(self, obj: Any, schema: dict) -> bool:
        for key, expected_type in schema.items():
            if key not in obj:
                return False
            if not isinstance(obj[key], expected_type):
                return False
        return True

v = AdvancedValidator()
schema = {"name": str, "age": int}
obj = {"name": "John", "age": 30}
print(v.validate(obj, schema))
