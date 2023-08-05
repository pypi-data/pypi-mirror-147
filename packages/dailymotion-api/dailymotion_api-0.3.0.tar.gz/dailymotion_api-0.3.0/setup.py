# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dailymotion_api',
 'dailymotion_api.routes',
 'dailymotion_api.static',
 'dailymotion_api.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'fastapi>=4.74.1,<5.0.0', 'uvicorn>=0.17.5,<0.18.0']

setup_kwargs = {
    'name': 'dailymotion-api',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'EmilRueda',
    'author_email': 'vladimir.rueda@udea.edu.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
