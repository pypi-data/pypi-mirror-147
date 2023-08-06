# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lieops',
 'lieops..ipynb_checkpoints',
 'lieops.linalg',
 'lieops.linalg..ipynb_checkpoints',
 'lieops.ops',
 'lieops.ops..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['mpmath>=1.2.1,<2.0.0', 'njet>=0.2.2,<0.3.0', 'sympy>=1.9,<2.0']

setup_kwargs = {
    'name': 'lieops',
    'version': '0.1.0',
    'description': 'Lie operator tools.',
    'long_description': None,
    'author': 'Malte Titze',
    'author_email': 'mtitze@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lieops.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
