# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging_utils_tddschn']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logging-utils-tddschn',
    'version': '0.1.2',
    'description': 'Logging utilities for my personal use.',
    'long_description': None,
    'author': 'Teddy Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
