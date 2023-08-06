# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_handler_exception']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.75.2,<0.76.0']

setup_kwargs = {
    'name': 'fastapi-handler-exception',
    'version': '0.1.1',
    'description': 'Provides a standard and quick way to add new error handlers to your fastapi application',
    'long_description': None,
    'author': 'Alan Vazquez',
    'author_email': 'alanvazquez1999@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
