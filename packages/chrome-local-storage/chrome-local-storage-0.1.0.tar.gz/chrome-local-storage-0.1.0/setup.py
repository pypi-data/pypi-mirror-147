# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chrome_local_storage']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0', 'trio-chrome-devtools-protocol>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'chrome-local-storage',
    'version': '0.1.0',
    'description': 'Interact with Chrome local storage',
    'long_description': None,
    'author': 'Judson Neer',
    'author_email': 'judson.neer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
