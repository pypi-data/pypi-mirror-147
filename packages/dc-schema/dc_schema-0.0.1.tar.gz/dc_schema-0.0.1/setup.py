# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dc_schema']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dc-schema',
    'version': '0.0.1',
    'description': 'Generate JSON schema from python dataclasses',
    'long_description': None,
    'author': 'Peter Byfield',
    'author_email': 'byfield554@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
