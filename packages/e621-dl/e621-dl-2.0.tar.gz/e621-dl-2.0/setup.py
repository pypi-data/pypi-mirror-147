# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['e621_dl']
install_requires = \
['click<8.1.0',
 'e621-temp>=0.0.2,<0.0.3',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.0.1,<13.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['e6 = e621_dl:app']}

setup_kwargs = {
    'name': 'e621-dl',
    'version': '2.0',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
