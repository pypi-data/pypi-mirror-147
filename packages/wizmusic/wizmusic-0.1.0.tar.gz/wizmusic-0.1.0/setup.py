# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wizmusic']

package_data = \
{'': ['*']}

install_requires = \
['colorgram.py>=1.2.0,<2.0.0', 'rich>=12.2.0,<13.0.0', 'spotipy>=2.19.0,<3.0.0']

entry_points = \
{'console_scripts': ['wizmusic = wizmusic.client:cli']}

setup_kwargs = {
    'name': 'wizmusic',
    'version': '0.1.0',
    'description': 'wiz spotify light',
    'long_description': None,
    'author': 'redraw',
    'author_email': 'redraw@sdf.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
