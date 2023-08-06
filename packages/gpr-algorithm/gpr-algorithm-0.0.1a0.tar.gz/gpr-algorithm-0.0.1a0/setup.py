# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpr_algorithm']

package_data = \
{'': ['*']}

install_requires = \
['deap==1.3.1',
 'geppy==0.1.3',
 'graphviz==0.19.1',
 'numpy==1.21.5',
 'scikit-learn==1.0.1',
 'sympy==1.9']

setup_kwargs = {
    'name': 'gpr-algorithm',
    'version': '0.0.1a0',
    'description': 'Gene Programming Rules (GPR) implementation',
    'long_description': 'GPR Algorithm\n=============\n\nGPR Algorithm is...\n\nHow to develop\n--------------\n\n1) Install Poetry: https://python-poetry.org/docs/#installation\n\n2) Initialize project:\n\n.. code-block::\n\n    poetry install\n',
    'author': 'Anna Czmil',
    'author_email': 'czmilanna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
