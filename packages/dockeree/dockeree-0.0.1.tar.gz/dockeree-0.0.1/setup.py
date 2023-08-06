# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockeree']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.0']

setup_kwargs = {
    'name': 'dockeree',
    'version': '0.0.1',
    'description': 'Make it easy to build and manager Docker images.',
    'long_description': None,
    'author': 'Benjamin Du',
    'author_email': 'longendu@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
