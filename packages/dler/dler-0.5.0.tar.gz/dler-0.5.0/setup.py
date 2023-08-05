# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dler', 'dler.cli', 'dler.tasker']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0',
 'm3u8>=1.0.0,<2.0.0',
 'multitasker>=0.0.2,<0.0.3',
 'requests>=2.27.1,<3.0.0',
 'typer>=0.4.1,<0.5.0',
 'wpy>=0.6.1,<0.7.0',
 'wsco>=0.0.1,<0.0.2']

entry_points = \
{'console_scripts': ['dler = dler.cli.main:app']}

setup_kwargs = {
    'name': 'dler',
    'version': '0.5.0',
    'description': 'python video downloader',
    'long_description': None,
    'author': 'wxnacy',
    'author_email': 'wxnacy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
