# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xkcd_cli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11,<5.0', 'requests>=2.27,<3.0', 'typer>=0.4,<0.5']

entry_points = \
{'console_scripts': ['xkcd = xkcd_cli.xkcd:main']}

setup_kwargs = {
    'name': 'dcs-xkcd-cli',
    'version': '0.1.0',
    'description': 'Get your daily dose of xkcd directly from the terminal! 🤩',
    'long_description': None,
    'author': 'dotcs',
    'author_email': 'repositories@dotcs.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
