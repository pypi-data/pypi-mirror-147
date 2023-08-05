# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['timestep']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'timestep',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Michael Schock',
    'author_email': 'm@mjschock.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
