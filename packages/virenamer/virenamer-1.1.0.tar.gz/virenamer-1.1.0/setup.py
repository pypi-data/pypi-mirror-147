# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virenamer']

package_data = \
{'': ['*']}

install_requires = \
['colorama']

entry_points = \
{'console_scripts': ['virenamer = virenamer.cli:run']}

setup_kwargs = {
    'name': 'virenamer',
    'version': '1.1.0',
    'description': 'Rename files by editing their paths directly in Vi (or in any other editor)',
    'long_description': None,
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
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
