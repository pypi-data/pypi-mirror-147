# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anytype']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'anytype',
    'version': '0.0.0',
    'description': 'Preserving a name for anytype.io library for Python,',
    'long_description': None,
    'author': 'Bobronium',
    'author_email': 'appkiller16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
