import sys
import orjson
from typing import Union

# Exception Error Classes
class InvalidSchema(Exception):
  """
  Raised when the defined schema is invalid.
  """
  pass

class InvalidJSON(Exception):
  """
  Raised when the JSON instance is not serializable.
  """
  pass

class ExpectedKey(Exception):
  """
  Encountered an expected key in the schema that is not in the instance.
  """
  pass

class UnexpectedKey(Exception):
  """
  Encountered an unexpected key that is not in the defined schema.
  """
  pass

class MaxSizeExceeded(Exception):
  """
  Raised when the JSON payload exceeds the max size bytes set.
  """
  pass

class TypeMismatch(Exception):
  """
  Raised when a value doesn't match the schema's expected datatype.
  """
  pass

class DidNotPassFunction(Exception):
  """
  Raised when a value does not pass a given validation function.
  """
  pass

# All validation functions lives here
class JSONValidator:
  def __init__(
    self,
    max_size_in_bytes = None,
    loosely_typed = False
  ):
    self.max_size_in_bytes = max_size_in_bytes
    self.loosely_typed = loosely_typed	

  def check_size(self, object):
    """
    Checks if the JSON payload exceeds the max bytes set.
    """
    if (self.max_size_in_bytes is not None) and (sys.getsizeof(object) > self.max_size_in_bytes):
      raise MaxSizeExceeded('The JSON payload ({} bytes) exceeds the set max size of {} bytes.'.format(
        sys.getsizeof(object),
        self.max_size_in_bytes
      ))

  def apply_type(self, value) -> Union[type, dict]:
    """
    Maps each value in a serialized object to it's data type.
    """
    dtype = type(value)

    # for inner dictionaries
    if dtype is dict:
      return self.create_schema(value)
    elif dtype is list:
      # unique set of data types for union type creation
      dtype_set = set()

      for elem in value:
        dtype_set.add(type(elem))

      if len(dtype_set) == 1:
        return list(dtype_set)
      else:
        union_set = Union[tuple(dtype_set)]
        return [union_set]

    return dtype

  def create_schema(self, instance: Union[str, dict]) -> dict:
    """
    Creates a structure based schema format.
    """
    if type(instance) == str: serialize = orjson.loads(instance)
    elif type(instance) == dict: serialize = instance
    else: raise InvalidJSON

    return {k: self.apply_type(v) for k, v in serialize.items()}

  def is_valid(
    self,
    instance: Union[str, dict],
    schema: dict
  ) -> bool:
    """
    A simple schema validation method that compares the serialized object
    to it's structural schema.
    """
    # checks if the JSON payload exceeds the max bytes set
    self.check_size(instance)

    if type(instance) == str: serialize = orjson.loads(instance)
    elif type(instance) == dict: serialize = instance
    else: raise InvalidJSON

    # create a dict where values are replaced by its data type
    # this basically creates a schema format
    mapped_dict = self.create_schema(serialize)

    return mapped_dict == schema

  def validate(
    self,
    instance: Union[str, dict], # accepts `dict` to make it analogous to the 'jsonschema' library
    schema: dict
  ) -> bool:
    """
    SCHEMA validation for complete object structure with options.
    """
    self.check_size(instance)

    if type(instance) == str: serialize = orjson.loads(instance)
    elif type(instance) == dict: serialize = instance
    else: raise InvalidJSON

    # check if all keys in the defined schema exists in the given instance
    for key, value in schema.items():
      if key not in serialize:
        raise ExpectedKey('Expected key `{}` in the given instance according to the defined schema.'.format(key))		  

    for key, value in serialize.items():
      # check if key exists
      if key not in schema:
        raise UnexpectedKey('Key `{}` does not exist in the defined schema.'.format(key))

      # checks if the data type matches that of the defined schema
      if not self.loosely_typed:
        schema_type = type(schema[key])
        allowed_dtypes = (type(type), dict, list)
        skip_ctx = False

        # verify that the schema is defined as datatype values
        if schema_type in allowed_dtypes or callable(schema[key]):
          if type(value) == schema[key]: continue

          if schema_type == dict:
            if not self.validate(instance=value, schema=schema[key]): raise TypeMismatch
            else: continue

          elif schema_type == list:
            if len(schema[key]) > 1:
              raise InvalidSchema(
                'List schema can only contain the acceptable datatype as value, ' \
                'to accept multiple datatypes: use `Union[]` instead.'
              )
            
            expected_type = schema[key][0]

            # type applied iterator over the serialized object
            for dtype in map(type, value):
              if dtype == expected_type: skip_ctx = True

              elif dtype == dict:
                if not self.validate(instance=value, schema=schema[key]): raise TypeMismatch
                else: skip_ctx = True

              elif '__args__' in vars(expected_type): # this handles the `Union` type
                if dtype not in expected_type.__args__:
                  raise TypeMismatch(
                    'Expected type `{}` for values in key `{}` (list) ' \
                    'but encountered `{}`.'.format(expected_type.__args__, key, dtype)
                  )
                else: skip_ctx = True

              else:
                raise TypeMismatch(
                  'Expected type `{}` for values in key `{}` (list) ' \
                    'but encountered `{}`.'.format(expected_type, key, dtype)
                )

          # handle function calls (like regex match function for example)
          elif callable(schema[key]):
            # execute the function if it returns true, it passes the validation
            # if it's an exception returning function, it will fail anyway.
            if schema[key](value): continue
            else:
              raise DidNotPassFunction('Value `{}` did not pass the function `{}()` [{}].'.format(
                value,
                schema[key].__name__,
                schema[key]
              ))

        else:
          # to retrieve function type
          def function(): pass

          # if it's a custom type class (like enums/functions/values), validate that
          # if not, the schema defined is not valid
          if schema_type in (type(value), type(function)): continue
          else:
            raise InvalidSchema(
              'Schema definition expected `{}` but encountered `{}`.'.format(schema[key], value)
            )

        if not skip_ctx and type(value) is not schema[key]:
          if schema_type == type(type): schema_type = schema[key]
          raise TypeMismatch(
            'Expected type `{}` for key `{}` but encountered `{}`.'.format(schema_type, key, type(value))
          )

    return True