# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mysqler']

package_data = \
{'': ['*']}

install_requires = \
['aiomysql>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'mysqler',
    'version': '0.1.0',
    'description': 'mysql for human.',
    'long_description': None,
    'author': 'tuna2134',
    'author_email': 'masato.04.11.2007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
