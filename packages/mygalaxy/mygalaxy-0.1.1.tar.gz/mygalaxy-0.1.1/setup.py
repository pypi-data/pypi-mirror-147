# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mygalaxy']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'mygalaxy',
    'version': '0.1.1',
    'description': 'A small galaxy to learn poetry',
    'long_description': None,
    'author': 'Gloria Macia',
    'author_email': 'g.macia-munoz@lse.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
