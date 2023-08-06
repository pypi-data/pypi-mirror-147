# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_package_matt2298', 'my_package_matt2298.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'my-package-matt2298',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matt Ellis',
    'author_email': 'matthew.ellis@sky.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
