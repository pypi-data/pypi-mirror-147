# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['combinatorapi',
 'combinatorapi.helper',
 'combinatorapi.helper.schemas',
 'combinatorapi.helper.web_scraper']

package_data = \
{'': ['*'], 'combinatorapi': ['.deta/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'fastapi>=0.75.1,<0.76.0',
 'requests>=2.27.1,<3.0.0',
 'uvicorn>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['start = combinatorapi.main:start']}

setup_kwargs = {
    'name': 'combinatorapi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'amarokkin',
    'author_email': 'jasminesingh.2011@gmail.com',
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
