# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['discord_app']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.1,<3.0.0', 'PyNaCl>=1.4.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'discord-app',
    'version': '0.0.1a0',
    'description': 'Discord interaction API wrapper',
    'long_description': None,
    'author': 'JackyCCC',
    'author_email': 'jacky9813@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
