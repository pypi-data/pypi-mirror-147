# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pxmcmc']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0.4,<6.0.0',
 'greatcirclepaths>=1.1.0,<2.0.0',
 'h5py>=3.3.0,<4.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pys2let>=2.2.3,<3.0.0',
 'pyssht>=1.4.0,<2.0.0',
 'scipy>=1.7.0,<1.8.0']

extras_require = \
{'cartopy': ['Cartopy>=0.19.0,<0.20.0'],
 'docs': ['sphinx>=4,<5', 'sphinx-rtd-theme==0.5']}

setup_kwargs = {
    'name': 'pxmcmc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Auggie Marignier',
    'author_email': 'augustin.marignier.14@ucl.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
