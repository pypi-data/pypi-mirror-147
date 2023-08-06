# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dgad', 'dgad.app', 'dgad.grpc', 'dgad.models']

package_data = \
{'': ['*'], 'dgad.grpc': ['protos/*']}

install_requires = \
['grpcio>=1,<2', 'keras-tcn>=3,<4', 'pandas>=1,<2', 'tldextract>=3,<4']

entry_points = \
{'console_scripts': ['dgad = dgad.app.cli:main']}

setup_kwargs = {
    'name': 'dgad',
    'version': '3.1.4',
    'description': 'Classifies DGA domains',
    'long_description': None,
    'author': 'Federico Falconieri',
    'author_email': 'federico.falconieri@tno.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
