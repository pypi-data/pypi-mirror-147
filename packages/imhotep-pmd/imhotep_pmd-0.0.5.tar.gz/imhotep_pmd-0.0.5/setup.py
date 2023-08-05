# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imhotep_pmd']

package_data = \
{'': ['*']}

install_requires = \
['imhotep>=2.0.0,<3.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'imhotep-pmd',
    'version': '0.0.5',
    'description': 'An Imhotep plugin for PMD, the static analyzer.',
    'long_description': None,
    'author': 'Mingyang Li',
    'author_email': 'tslmy@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
