# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['based', 'based.cli', 'based.cli.based', 'based.converters', 'based.standards']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0', 'frozendict>=2.3.2,<3.0.0', 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'pybased',
    'version': '0.0.1',
    'description': 'Library for creating arbitrary binary encodings.  Includes variations on base32, base64, base85, and more.',
    'long_description': "# based\n\nLibrary for creating arbitrary binary encodings.  Includes variations on base32, base64, base85, and more.\n\n## Getting started\n\n```shell\n$ pip install pybased\n```\n\n## Doing stuff\n```python\n# Lets's assume we want to use the Crockford32 encoding scheme.\nfrom based.standards.base32 import crockford32\n\n# And let's assume the variable data has what we want to encode.\ndata: bytes = ...\n\n# Encode to string.\nencoded: str = crockford32.encode_bytes(data)\n\n# ...\n\n# Decode the string back to bytes.\ndata: bytes = crockford32.decode_bytes(encoded)\n```\n\n## `based` Command-Line Tool\n\n`based --help`\n\nNOTE: This is generally only useful for testing.",
    'author': 'Rob Nelson',
    'author_email': 'nexisentertainment@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/N3X15/python-based',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
