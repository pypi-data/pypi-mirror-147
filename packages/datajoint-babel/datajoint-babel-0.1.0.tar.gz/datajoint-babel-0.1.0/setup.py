# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datajoint_babel', 'datajoint_babel.model']

package_data = \
{'': ['*']}

install_requires = \
['datajoint>=0.13.4,<0.14.0', 'parse>=1.19.0,<2.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'datajoint-babel',
    'version': '0.1.0',
    'description': 'Generate schema code from model definitions for both Python and MATLAB',
    'long_description': None,
    'author': 'sneakers-the-rat',
    'author_email': 'JLSaunders987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
