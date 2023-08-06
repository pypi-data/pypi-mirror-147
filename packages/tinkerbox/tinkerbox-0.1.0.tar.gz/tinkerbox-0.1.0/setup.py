# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinkerbox', 'tinkerbox.bplustree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tinkerbox',
    'version': '0.1.0',
    'description': 'tidbits to play around with',
    'long_description': None,
    'author': 'Subodh Lamichhane',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
