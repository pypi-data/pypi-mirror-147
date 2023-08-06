# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ziptool']

package_data = \
{'': ['*'], 'ziptool': ['resources/zip_tract_122021.parquet']}

install_requires = \
['Rtree>=0.9.7,<0.10.0',
 'fastparquet>=0.8.0,<0.9.0',
 'geopandas>=0.10.2,<0.11.0',
 'ipumspy>=0.1.0,<0.2.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'us>=2.0.2,<3.0.0',
 'wquantiles>=0.6,<0.7']

setup_kwargs = {
    'name': 'ziptool',
    'version': '0.0.1.dev7',
    'description': 'A tool for aggregating Census data at the ZIP code level',
    'long_description': "[![Documentation Status](https://readthedocs.org/projects/ziptool/badge/?version=latest)](https://ziptool.readthedocs.io/en/latest/?badge=latest)\n\n# ZIPtool\n\nThis tool is designed to analyze microdata from the American Community Survey (ACS) on a ZIP-code level. The Census Bureau publishes microdata only on a Public Use Microdata Area (PUMA) basis, so this package converts ZIP to PUMA and returns the relevant data as either summary statistics or the raw data.\n\n### Requirements\n\nThis project requires Python 3.8.0 or higher. Install using:\n\n### Getting Started\n\nYou can find the project's documentation <a href = https://ziptool.readthedocs.io/>here</a>.\n\n### Development\n\nThis project is in the early stages of development, so please email <a href = mailto:joshua_neronha@brown.edu>joshua_neronha@brown.edu</a> with any problems you may encounter!\n",
    'author': 'Joshua Neronha',
    'author_email': 'joshua_neronha@brown.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joshuaneronha/ziptool',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
