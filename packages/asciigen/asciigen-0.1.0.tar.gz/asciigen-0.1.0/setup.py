# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asciigen']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'opencv-python>=4.5.5,<5.0.0', 'urwid>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['asciigen = asciigen.main:cli']}

setup_kwargs = {
    'name': 'asciigen',
    'version': '0.1.0',
    'description': 'Ascii art image generator',
    'long_description': None,
    'author': 'Juan Lara',
    'author_email': 'julara@unal.edu.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
