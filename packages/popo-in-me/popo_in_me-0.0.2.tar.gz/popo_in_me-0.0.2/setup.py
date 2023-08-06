# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['popo_in_me', 'popo_in_me.popo_in_me', 'popo_in_me.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'popo-in-me',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
