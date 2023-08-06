# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ready_logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ready-logger',
    'version': '0.1.2',
    'description': 'Easily configure loggers.',
    'long_description': None,
    'author': 'Dan Kelleher',
    'author_email': 'dan@danklabs.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
