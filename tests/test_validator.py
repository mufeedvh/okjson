from okjson import JSONValidator
from typing import Union

def test_empty():
	schema = {}
	json = "{}"

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).validate(instance=json, schema=schema)

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).is_valid(instance=json, schema=schema)

def test_basic():
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

	json_string = """
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
	).validate(instance=json_string, schema=schema)

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).is_valid(instance=json_string, schema=schema)

def test_basic_with_union():
	schema = {
		'name': str,
		'age': int,
		'marks': {
			'english': float,
			'science': float,
			'mathematics': float,
			'computer_science': float
		},
		'random': [Union[str, int, float]]
	}

	json_string = """
	{
		"name": "Charly Gordon",
		"age": 32,
		"marks": {
			"english": 69.4,
			"science": 13.7,
			"mathematics": 10.3,
			"computer_science": 96.4
		},
		"random": ["computer whiz", 6.9, 4, 2, 0]
	}
	"""

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).validate(instance=json_string, schema=schema)

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).is_valid(instance=json_string, schema=schema)

def test_function_call():
	import re

	email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

	schema = {
		'email': email_regex.match,
		'password': str
	}

	json_string = """
	{
		"email": "test@mail.com",
		"password": "hunter2"
	}
	"""

	assert JSONValidator(
		max_size_in_bytes=1000,
		loosely_typed=False
	).validate(instance=json_string, schema=schema)