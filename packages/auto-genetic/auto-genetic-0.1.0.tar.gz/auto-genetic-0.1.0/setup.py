# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_genetic',
 'auto_genetic.evaluation',
 'auto_genetic.population_initializer',
 'auto_genetic.reproduction']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0', 'sklearn>=0.0,<0.1', 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'auto-genetic',
    'version': '0.1.0',
    'description': 'a package for automatic hyperparameter tuning or feature selection, using a genetic algorithm',
    'long_description': None,
    'author': 'Tommaso Corato',
    'author_email': 'tommaso.corato@glovoapp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
