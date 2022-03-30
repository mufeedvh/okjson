from okjson import JSONValidator

# a valid/expected format of JSON
expected_valid_json = open('tests/twitter.json', 'r').read()

# create a schema with it
expected_valid_schema = JSONValidator().create_schema(expected_valid_json)

# validate `instances` with the created schema
assert JSONValidator().validate(instance=expected_valid_json, schema=expected_valid_schema)