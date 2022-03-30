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
    description = 'A fast, simple, and pythonic JSON Schema Validator.',
    author = 'Mufeed VH',
    author_email = 'contact@mufeedvh.com',
    url = 'https://github.com/mufeedvh/okjson',
    download_url = 'https://github.com/mufeedvh/okjson/archive/refs/tags/v0.1.0.tar.gz',
    keywords = ['json', 'schema', 'jsonschema', 'validation', 'validator'],
    license = 'MIT'
)