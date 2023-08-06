# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mrchef']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0.1',
 'decorator>=5.1.1',
 'git-autoshare>=1.0.0-beta.6',
 'mergedeep>=1.3.4',
 'platformdirs<2.5.2',
 'plumbum>=1.7.2',
 'requests>=2.27.1',
 'tomlkit>=0.10.0',
 'xdg>=5.1.1']

entry_points = \
{'console_scripts': ['mrchef = mrchef.__main__:run']}

setup_kwargs = {
    'name': 'mrchef',
    'version': '0.2.1',
    'description': 'Metarepo Chef',
    'long_description': None,
    'author': 'Moduon',
    'author_email': 'info@moduon.team',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
