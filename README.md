<div align="center">
    <h1>{ <code>okjson</code> }</h1>
    <p>A fast, simple, and pythonic JSON Schema Validator</p>
    <a href="#usage">Usage</a> • <a href="#install">Install</a> • <a href="#features">Features</a> • <a href="#benchmarks">Benchmarks</a> • <a href="#license">License</a>
</div>

## Install

```
$ pip install okjson==0.1.1
```

**⚠️ NOTE:** This library has not been battle-tested, please don't use this in production. yet.

## Features

- **Simplicity:** The schema definition is pythonic in the sense that you can directly specify the expected data type with the corresponding keyword. This is inspired by the design of [tiangolo/sqlmodel](https://github.com/tiangolo/sqlmodel).
- **Performance:** Just 250ish lines of simple and optimized code, performs better than the alternatives simply because it does relatively less work. It also uses [orjson](https://github.com/ijl/orjson) under the hood for serialization if you're providing a raw JSON string as input.  (See [Benchmarks](#benchmarks))
- **Composability:** You can write your own validation function for values, all it has to do is return `True` on a valid input just like the `regex` example below. (See [Usage](https://github.com/mufeedvh/okjson_bak#every-feature-in-a-single-example))
- **Options:** The `max_size_in_bytes` option allows you to prevent processing large payloads (in web/network scenarios) and you can opt out of data type validation with the `loosely_typed` option.
- **Helpful Error Messages:** The `validate()` function prints out helpful exception messages for easier debugging.

## Usage

### A basic example showing how the library works:

For simple schemas where you just want to validate if the structure and data type of the values match, use the `is_valid()` method.

```py
from okjson import JSONValidator

schema = { 'name': str, 'age': int }

json_string = '{ "name": "Charly Gordon", "age": 32 }'

assert JSONValidator().is_valid(instance=json_string, schema=schema)
```

### Every feature in a single example:

For any schema that includes inner dictonaries/lists or cusom validation functions, use the `validate()` method instead.

**Tip:** Just like how the regex match function is utilized in this example, you can compose any function, all that's required is that it returns `True` if it passes the validation.

```py
from okjson import JSONValidator
from typing import Union

import re
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

schema = {
    'email': email_regex.match, # the value of `email` should match to the compiled email regex above
    'password': str, # password is of type `str`
    'user': {
        'token': str, # token is of type `str`
        'badges': [str], # this list can only contain `str` elements
        'values': [Union[str, float]] # this list can contain both `str` and `float` elements
    }
}

json_string = """
{
    "email": "test@mail.com",
    "password": "hunter2",
    "user": {
        "token": "d08f46c929b5098b61105fdf6e24d014",
        "badges": ["OG"],
        "values": ["test", 69.420]
    }
}
"""

assert JSONValidator().validate(instance=json_string, schema=schema)
```

### Validating against a large schema:

Got a large schema to make? Just call the `create_schema()` function on a valid JSON file that follows the desired schema.

**⚠️ NOTE:** This currently does not validate nested dictionaries!

```py
from okjson import JSONValidator

# a valid/expected format of JSON
expected_valid_json = open('tests/twitter.json', 'r').read()

# create a schema with it
expected_valid_schema = JSONValidator().create_schema(expected_valid_json)

# validate `instances` with the created schema
assert JSONValidator().validate(instance=expected_valid_json, schema=expected_valid_schema)
```

### Extra options for validation:

```py
assert JSONValidator(
    max_size_in_bytes=1000, # payload shouldn't exceed 1000 bytes
    loosely_typed=False # types should be checked (strongly typed)
).validate(instance=json_string, schema=schema)
```

**What's the difference between methods `is_valid()` and `validate()`?**

The `is_valid()` function only checks for the schema structure for correctness thus faster than `validate()`. The `validate()` function checks the schema structure along with the configurable options and handles exceptions with verbose error messages. There is no drastic performance difference betwen the two. Both are significantly fast in comparison to other schema validation libraries.

**NOTE:** You can also pass in the result of `json.loads()` for the `instance` value instead of the raw JSON string.

## Benchmarks

> **NOTE:** This is not an "apples to apples" comparison since this library works entirely differently to that of the ones in comparison here. Both of the other libraries are an implementation of the [JSON Schema Specification](https://json-schema.org/). However, this library serves the exact same purpose with a simpler solution with more composability (callable custom functions for example) and performance benefits.

```
$ python3 benchmarks/benchmarks.py
[-] Basic Bench okjson `is_valid()` 1000 runs: 0.004736766999485553
[-] Basic Bench okjson `validate()` 1000 runs: 0.007322061999730067
[-] Basic Bench jsonschema 1000 runs: 1.4104747559995303
[-] Basic Bench fastjsonschema 1000 runs: 0.5503115159999652

okjson is 116x faster than fastjsonschema
fastjsonschema is 2x faster than jsonschema

[-] okjson `is_valid()` example 1000 runs: 0.0018266600000060862
[-] okjson `validate()` example 1000 runs: 0.0020380820005811984
[-] jsonschema example 1000 runs: 1.1857670320005127
[-] fastjsonschema example 1000 runs: 0.3467409430004409

okjson is 189x faster than fastjsonschema
fastjsonschema is 3x faster than jsonschema
```

## Contribution

Ways to contribute:

- Suggest a feature
- Report a bug
- Fix something and open a pull request
- Help me document the code
- Spread the word

## License

Licensed under the MIT License, see <a href="https://github.com/mufeedvh/okjson/blob/master/LICENSE">LICENSE</a> for more information.
