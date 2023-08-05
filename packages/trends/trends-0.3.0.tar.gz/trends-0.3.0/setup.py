# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trends']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trends',
    'version': '0.3.0',
    'description': 'Generate and study quasi-monotonic sequences.',
    'long_description': None,
    'author': 'Jeffrey S. Haemer',
    'author_email': 'jeffrey.haemer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
