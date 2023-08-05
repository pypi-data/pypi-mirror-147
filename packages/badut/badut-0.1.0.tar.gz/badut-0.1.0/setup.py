# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['badut', 'badut.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'badut',
    'version': '0.1.0',
    'description': 'Python HTTP client designed to be simple in async context',
    'long_description': None,
    'author': 'sinkaroid',
    'author_email': 'anakmancasan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
