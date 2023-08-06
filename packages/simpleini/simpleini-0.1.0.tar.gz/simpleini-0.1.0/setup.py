# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleini']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['APPLICATION-NAME = __init__:main']}

setup_kwargs = {
    'name': 'simpleini',
    'version': '0.1.0',
    'description': 'Simple use ini files',
    'long_description': None,
    'author': 'to101',
    'author_email': 'to101kv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
