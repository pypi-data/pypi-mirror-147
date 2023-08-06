# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testouillos']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'testouillos',
    'version': '0.0.4',
    'description': 'A simple test',
    'long_description': None,
    'author': 'Yann Rabiller',
    'author_email': 'yann.rabiller@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Einenlum/testouillos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
