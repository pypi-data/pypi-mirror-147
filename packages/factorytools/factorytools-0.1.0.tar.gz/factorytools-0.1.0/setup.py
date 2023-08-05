# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factorytools']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.0,<5.0', 'factory_boy>=3.2,<4.0']

setup_kwargs = {
    'name': 'factorytools',
    'version': '0.1.0',
    'description': 'Assistive tools for factoryboy',
    'long_description': None,
    'author': 'Jayson Dorsett',
    'author_email': 'ja_dorsett@jdorsett.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
