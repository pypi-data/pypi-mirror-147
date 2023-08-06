# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextchat']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nextchat',
    'version': '1.0.0.2',
    'description': 'Easy to use bot API for https://replchat.vapwastaken.repl.co/',
    'long_description': None,
    'author': 'Bleekpie',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
