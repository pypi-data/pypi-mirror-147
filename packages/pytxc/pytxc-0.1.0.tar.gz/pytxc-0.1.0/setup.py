# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytxc']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.1,<2.0.0',
 'lxml>=4.7.1,<5.0.0',
 'pyproj>=3.3.0,<4.0.0',
 'shapely-geojson>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'pytxc',
    'version': '0.1.0',
    'description': 'Python parser from TransXChange.',
    'long_description': None,
    'author': 'Ciaran McCormick',
    'author_email': 'ciaran@ciaranmccormick.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
