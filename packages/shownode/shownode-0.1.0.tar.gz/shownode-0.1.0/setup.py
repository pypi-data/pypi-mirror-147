# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shownode']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['shownode = shownode.shownode:cli']}

setup_kwargs = {
    'name': 'shownode',
    'version': '0.1.0',
    'description': 'Connect to docker containers with open vnc ports',
    'long_description': None,
    'author': 'dskard',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
