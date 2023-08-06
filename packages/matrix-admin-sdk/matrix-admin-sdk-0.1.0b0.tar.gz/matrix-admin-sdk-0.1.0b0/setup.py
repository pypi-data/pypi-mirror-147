# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrix_admin_sdk',
 'matrix_admin_sdk.endpoints',
 'matrix_admin_sdk.endpoints.v1',
 'matrix_admin_sdk.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'matrix-admin-sdk',
    'version': '0.1.0b0',
    'description': '',
    'long_description': None,
    'author': 'Dmitrii Kurlov',
    'author_email': 'dmitriik@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
