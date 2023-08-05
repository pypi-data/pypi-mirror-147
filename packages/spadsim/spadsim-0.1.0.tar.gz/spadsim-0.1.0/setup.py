# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spadsim']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.1.1',
 'dask>=2022.01.1',
 'distributed>=2022.01.1',
 'ipykernel>=6',
 'ipywidgets>=7.7.0,<8.0.0',
 'matplotlib>=3',
 'numba>=0.55',
 'numpy>=1.18',
 'pandas>=1.3',
 'tqdm>=4.3']

setup_kwargs = {
    'name': 'spadsim',
    'version': '0.1.0',
    'description': 'This is a 2D Monte Carlo simulator written in Python to model the operation of single-photon avalanche detectors. It simulates the stochastic avalanche multiplication process of charge carriers following the absorption of an input photon; a successful detection event is defined as the avalanche current exceeding a pre-defined threshold. The simulator output can be used to analyse the photon detection efficiency and its timing characteristics. This program does not directly simulate dark noise.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
