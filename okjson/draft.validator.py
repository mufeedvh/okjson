import sys
import orjson
from typing import Union, Any

class ValidationError(Exception):
    pass

class JSONValidator:
    def __init__(self, max_size_in_bytes: int = None, loosely_typed: bool = False):
        self.max_size_in_bytes = max_size_in_bytes
        self.loosely_typed = loosely_typed

    def check_size(self, payload: str):
        size_in_bytes = len(payload.encode('utf-8'))
        if self.max_size_in_bytes and size_in_bytes > self.max_size_in_bytes:
            raise ValidationError(f'Payload size ({size_in_bytes} bytes) exceeds max size of {self.max_size_in_bytes} bytes.')

    def deserialize(self, instance: Union[str, dict]) -> dict:
        if isinstance(instance, str):
            return orjson.loads(instance)
        elif isinstance(instance, dict):
            return instance
        else:
            raise ValidationError('Invalid JSON input.')

    def apply_type(self, value: Any) -> Union[type, dict, list]:
        if isinstance(value, dict):
            return self.create_schema(value)
        elif isinstance(value, list):
            dtype_set = {type(elem) for elem in value}
            return [Union[tuple(dtype_set)]] if len(dtype_set) > 1 else [next(iter(dtype_set))]
        return type(value)

    def create_schema(self, instance: Union[str, dict]) -> dict:
        return {k: self.apply_type(v) for k, v in self.deserialize(instance).items()}

    def validate_value(self, value: Any, schema_type: Any) -> bool:
        if isinstance(schema_type, type) and isinstance(value, schema_type):
            return True
        elif isinstance(schema_type, list) and all(self.validate_value(v, schema_type[0]) for v in value):
            return True
        elif isinstance(schema_type, dict) and self.validate(value, schema_type):
            return True
        elif callable(schema_type) and schema_type(value):
            return True
        return False

    def validate(self, instance: Union[str, dict], schema: dict) -> bool:
        self.check_size(instance if isinstance(instance, str) else orjson.dumps(instance).decode('utf-8'))
        serialized_instance = self.deserialize(instance)

        for key, value in schema.items():
            if key not in serialized_instance:
                raise ValidationError(f'Expected key `{key}` missing in instance.')

            if key not in schema:
                raise ValidationError(f'Unexpected key `{key}` in instance.')

            if not self.loosely_typed and not self.validate_value(serialized_instance[key], value):
                raise ValidationError(f'Type mismatch for key `{key}`. Expected {value} but got {type(serialized_instance[key])}.')

        return True
