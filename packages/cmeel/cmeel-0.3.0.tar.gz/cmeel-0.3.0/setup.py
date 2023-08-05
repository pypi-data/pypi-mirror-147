# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cmeel']
install_requires = \
['cmake>=3.22.3,<4.0.0', 'tomli>=2.0.1,<3.0.0', 'wheel>=0.37.1,<0.38.0']

setup_kwargs = {
    'name': 'cmeel',
    'version': '0.3.0',
    'description': 'Create Wheel from CMake projects',
    'long_description': None,
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
