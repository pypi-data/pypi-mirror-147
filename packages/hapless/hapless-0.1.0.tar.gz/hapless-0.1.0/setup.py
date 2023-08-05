# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hapless']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'humanize>=4.0.0,<5.0.0',
 'psutil>=5.9.0,<6.0.0',
 'rich>=12.2.0,<13.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.11.3,<5.0.0']}

entry_points = \
{'console_scripts': ['hap = hapless.cli:cli']}

setup_kwargs = {
    'name': 'hapless',
    'version': '0.1.0',
    'description': 'Run and track processes in background',
    'long_description': None,
    'author': 'Misha Behersky',
    'author_email': 'bmwant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
