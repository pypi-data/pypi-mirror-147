# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lidar_pbl', 'lidar_pbl.cli', 'lidar_pbl.core', 'lidar_pbl.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'rich>=12.0.0,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['lidar-pbl = lidar_pbl.cli.app:run']}

setup_kwargs = {
    'name': 'lidar-pbl',
    'version': '0.1.0',
    'description': 'Package in development that contains functions and command line utitlities to handle lidar data and PBL height calculations',
    'long_description': None,
    'author': 'Juan Diego',
    'author_email': 'jdidelarc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdlar1/lidar-pbl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
