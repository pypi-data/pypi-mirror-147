# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['siteup']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0']

setup_kwargs = {
    'name': 'siteup',
    'version': '0.1.0',
    'description': 'cli tool to check online status of websites',
    'long_description': None,
    'author': 'BrianLusina',
    'author_email': '12752833+BrianLusina@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
