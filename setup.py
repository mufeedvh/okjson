from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # package
    name = 'okjson',
    packages = find_packages(include=['okjson']),
    install_requires = ['orjson'],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    test_suite = 'tests',

    # metadata
    version = '0.1.1',
    description = 'A fast, simple, and pythonic JSON Schema Validator.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Mufeed VH',
    author_email = 'contact@mufeedvh.com',
    url = 'https://github.com/mufeedvh/okjson',
    download_url = 'https://github.com/mufeedvh/okjson/archive/refs/tags/v0.1.1.tar.gz',
    keywords = ['json', 'schema', 'jsonschema', 'validation', 'validator'],
    license = 'MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
)
