# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipchanger']

package_data = \
{'': ['*']}

install_requires = \
['pyelftools>=0.28,<0.29']

entry_points = \
{'console_scripts': ['ipchanger = ipchanger:run']}

setup_kwargs = {
    'name': 'tibia-ipchanger',
    'version': '0.1.1',
    'description': 'Command-line IP changer for Tibia clients (Linux only)',
    'long_description': 'tibia-ipchanger\n===============\n',
    'author': 'Ranieri Althoff',
    'author_email': 'ranisalt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ranisalt/tibia-ipchanger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
