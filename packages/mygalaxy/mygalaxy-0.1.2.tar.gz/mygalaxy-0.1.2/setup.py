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
    'version': '0.1.2',
    'description': 'A small galaxy to learn poetry',
    'long_description': "# mygalaxy \n\nA small galaxy to learn poetry. \n\n## How to install \n\n`pip install mygalaxy`\n\n## How to use\n\n### Create your planet\n\n    from mygalaxy.planet import Planet\n    earth = Planet(name='earth', radius=6371000, gravity=9.807, system='solar')\n    print(earth.gravity)\n\n### Make your planet spin \n\n`earth.spin()`\n\n### Make your planet orbit\n\n`earth.orbit()`\n\n### Learn the shape of your planet\n\n`earth.commons()`\n\n\n### Compute the mass of your planet\n\n`earth.mass()`\n\n\n### Compute the volume of your planet \n\n`earth.volume()`\n\nYou may also use the mass and volume compute functions separately by doing: \n\n    from mygalaxy.calc import planet_mass, planet_vol\n    r = 6371000\n    g = 9.807\n    print(planet_mass(gravity=g, radius=r))\n    print(planet_vol(radius=r))\n\n### Related URLs\n* https://python-poetry.org/\n* https://realpython.com/dependency-management-python-poetry/\n* https://www.youtube.com/watch?v=f26nAmfJggw\n* https://realpython.com/pypi-publish-python-package/\n* https://www.youtube.com/watch?v=sugvnHA7ElY&t=242s\n* https://stackoverflow.com/a/70027834/7762646\n\n\n\n",
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
