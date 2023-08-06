# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typeany']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'typeany',
    'version': '0.1.0',
    'description': 'Preserving a cool name for Pythonn library for anytype.io. type[Any].',
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
