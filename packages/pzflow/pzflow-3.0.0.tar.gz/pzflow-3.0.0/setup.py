# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pzflow']

package_data = \
{'': ['*'], 'pzflow': ['example_files/*']}

install_requires = \
['dill>=0.3.4,<0.4.0',
 'jax>=0.3.5,<0.4.0',
 'jaxlib>=0.3.5,<0.4.0',
 'optax>=0.1.2,<0.2.0',
 'pandas>=1.1',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'pzflow',
    'version': '3.0.0',
    'description': 'Probabilistic modeling of tabular data with normalizing flows.',
    'long_description': None,
    'author': 'John Franklin Crenshaw',
    'author_email': 'jfcrenshaw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
