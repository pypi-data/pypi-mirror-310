# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fantasy_agn']

package_data = \
{'': ['*'], 'fantasy_agn': ['eigen/*', 'input/*', 'sfddata/*']}

install_requires = \
['PyAstronomy==0.17.1',
 'RegscorePy==1.1',
 'astropy>4.3.1',
 'matplotlib==3.4.3',
 'natsort==8.1.0',
 'numpy>1.21',
 'pandas==1.3.4',
 'scikit-learn>1.0.2',
 'scipy>=1.8.0,<2.0.0',
 'sfdmap2==0.2.2',
 'sherpa>4.14.0',
 'spectres==2.1.1']

setup_kwargs = {
    'name': 'fantasy-agn',
    'version': '1.0.0',
    'description': ' FANTASY - Fully Automated pythoN tool for AGN Spectra analYsis, a python based code for simultaneous multi-component fitting of AGN spectra, optimized for the optical rest-frame band (3600-8000A), but also applicable to the UV range (2000-3600A) and NIR range (8000-11000A).',
    'long_description': None,
    'author': 'Nemanja',
    'author_email': 'rakinemanja@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<=3.12',
}


setup(**setup_kwargs)
