# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kubeseal_auto']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.2,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'icecream>=2.1.2,<3.0.0',
 'kubernetes>=23.3.0,<24.0.0',
 'questionary>=1.10.0,<2.0.0']

entry_points = \
{'console_scripts': ['kubeseal-auto = kubeseal_auto.cli:cli']}

setup_kwargs = {
    'name': 'kubeseal-auto',
    'version': '0.2.0',
    'description': 'An interactive wrapper for kubeseal binary',
    'long_description': None,
    'author': 'Vadim Gedz',
    'author_email': 'vadims@linux-tech.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
