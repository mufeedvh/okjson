from jsonschema import validate
import fastjsonschema
from okjson import JSONValidator

import json
import timeit

def bench_basic_is_valid_okjson():
	schema = {
		'name': str,
		'age': int,
		'marks': {
			'english': float,
			'science': float,
			'mathematics': float,
			'computer_science': float
		},
		'badges': [str]
	}

	instance = """
	{
		"name": "Charly Gordon",
		"age": 32,
		"marks": {
			"english": 69.4,
			"science": 13.7,
			"mathematics": 10.3,
			"computer_science": 96.4
		},
		"badges": ["computer whiz"]
	}
	"""

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).is_valid(instance=instance, schema=schema)

def bench_basic_okjson():
	schema = {
		'name': str,
		'age': int,
		'marks': {
			'english': float,
			'science': float,
			'mathematics': float,
			'computer_science': float
		},
		'badges': [str]
	}

	instance = """
	{
		"name": "Charly Gordon",
		"age": 32,
		"marks": {
			"english": 69.4,
			"science": 13.7,
			"mathematics": 10.3,
			"computer_science": 96.4
		},
		"badges": ["computer whiz"]
	}
	"""

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).validate(instance=instance, schema=schema)

def bench_basic_jsonschema():
	schema = {
        "type" : "object",
        "properties" : {
            "name" : {"type" : "string"},
            "age" : {"type" : "number"},
            "marks" : {
                "type" : "object",
                "english" : {"type" : "number"},
                "science" : {"type" : "number"},
                "mathematics" : {"type" : "number"},
                "computer_science" : {"type" : "number"}
            },
            "badges" : {"type": "array"}
        },
	}

	instance = json.loads("""
	{
		"name": "Charly Gordon",
		"age": 32,
		"marks": {
			"english": "s",
			"science": 13.7,
			"mathematics": 10.3,
			"computer_science": 96.4
		},
		"badges": ["computer whiz"]
	}
	""")

	assert validate(instance=instance, schema=schema) == None

def bench_basic_fastjsonschema():
	validate = fastjsonschema.compile({
        "type" : "object",
        "properties" : {
            "name" : {"type" : "string"},
            "age" : {"type" : "number"},
            "marks" : {
                "type" : "object",
                "english" : {"type" : "number"},
                "science" : {"type" : "number"},
                "mathematics" : {"type" : "number"},
                "computer_science" : {"type" : "number"}
            },
            "badges" : {"type": "array"}
        },
	})

	instance = json.loads("""
	{
		"name": "Charly Gordon",
		"age": 32,
		"marks": {
			"english": "s",
			"science": 13.7,
			"mathematics": 10.3,
			"computer_science": 96.4
		},
		"badges": ["computer whiz"]
	}
	""")

	assert validate(instance) != None

def okjson_is_valid_example():
    schema = {
        'name': str,
        'price': float
    }
    
    assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).is_valid(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

def okjson_example():
    schema = {
        'name': str,
        'price': float
    }
    
    assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

def jsonschema_example():
    schema = {
        "type" : "object",
        "properties" : {
            "price" : {"type" : "number"},
            "name" : {"type" : "string"},
        },
    }

    assert validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema) == None    

def fastjsonschema_example():
    validate = fastjsonschema.compile({
        "type" : "object",
        "properties" : {
            "price" : {"type" : "number"},
            "name" : {"type" : "string"},
        },
    })

    assert validate({"name" : "Eggs", "price" : 34.99}) != None

"""
Bench Basic
"""
okjson_is_valid_time = timeit.timeit(bench_basic_is_valid_okjson, number=1000)
print("[-] Basic Bench okjson `is_valid()` 1000 runs: {}".format(okjson_is_valid_time))
okjson_time = timeit.timeit(bench_basic_okjson, number=1000)
print("[-] Basic Bench okjson `validate()` 1000 runs: {}".format(okjson_time))
jsonschema_time = timeit.timeit(bench_basic_jsonschema, number=1000)
print("[-] Basic Bench jsonschema 1000 runs: {}".format(jsonschema_time))
fastjsonschema_time = timeit.timeit(bench_basic_fastjsonschema, number=1000)
print("[-] Basic Bench fastjsonschema 1000 runs: {}".format(fastjsonschema_time))

print("\nokjson is {}x faster than fastjsonschema".format(int(fastjsonschema_time / okjson_is_valid_time)))
print("fastjsonschema is {}x faster than jsonschema\n".format(int(jsonschema_time / fastjsonschema_time)))

"""
Bench Example
"""
okjson_is_valid_time = timeit.timeit(okjson_is_valid_example, number=1000)
print("[-] okjson `is_valid()` example 1000 runs: {}".format(okjson_is_valid_time))
okjson_time = timeit.timeit(okjson_example, number=1000)
print("[-] okjson `validate()` example 1000 runs: {}".format(okjson_time))
jsonschema_time = timeit.timeit(jsonschema_example, number=1000)
print("[-] jsonschema example 1000 runs: {}".format(jsonschema_time))
fastjsonschema_time = timeit.timeit(fastjsonschema_example, number=1000)
print("[-] fastjsonschema example 1000 runs: {}".format(fastjsonschema_time))

print("\nokjson is {}x faster than fastjsonschema".format(int(fastjsonschema_time / okjson_is_valid_time)))
print("fastjsonschema is {}x faster than jsonschema".format(int(jsonschema_time / fastjsonschema_time)))