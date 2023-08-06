# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psychoanalyze']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'psychoanalyze',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tyler Schlichenmeyer',
    'author_email': 'tyler.schlichenmeyer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
