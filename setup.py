from setuptools import find_packages, setup

setup(
	# package
    name = 'okjson',
    packages = find_packages(include=['okjson']),
    install_requires = ['orjson'],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    test_suite = 'tests',

    # metadata
    version = '0.1.0',
    description = 'Fast and strongly typed JSON Schema validator for Python.',
    author = 'Mufeed VH',
    license = 'MIT',
)