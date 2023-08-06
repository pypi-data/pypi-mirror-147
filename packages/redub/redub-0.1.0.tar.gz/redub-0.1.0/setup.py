# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redub']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.59.0,<5.0.0', 'openpyxl>=3.0.9,<4.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'redub',
    'version': '0.1.0',
    'description': 'an app for renaming an entire directory of images using an excel spreadsheet',
    'long_description': None,
    'author': 'David Flood',
    'author_email': 'davidfloodii@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
