# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual',
 'textual.drivers',
 'textual.layouts',
 'textual.views',
 'textual.widgets']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.0.0,<13.0.0', 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'textual-stub',
    'version': '0.1.17',
    'description': 'Text User Interface using Rich',
    'long_description': '# WARNING\nThis package is published as a temporary copy of textual. It **will** be deleted once textual upgrades their typing_extensions to support the features of python 3.11. DO NOT use it in any way.',
    'author': 'Will McGugan',
    'author_email': 'willmcgugan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willmcgugan/textual',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
