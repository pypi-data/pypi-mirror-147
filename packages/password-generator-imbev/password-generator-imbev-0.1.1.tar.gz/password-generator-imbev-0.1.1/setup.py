# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['password_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'password-generator-imbev',
    'version': '0.1.1',
    'description': 'A password generator written in Python.',
    'long_description': None,
    'author': 'Isaac Beverly',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
