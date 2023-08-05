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
    'version': '2.0.4',
    'description': 'A simple and fast e621 post/pool downloader',
    'long_description': '# e621-dl\n**e621-dl** is a simple and fast e621 post/pool downloader. It is based upon the [e621](https://github.com/PatriotRossii/e621-py) api wrapper both in implementation and interface.\n\n## Installation\n`pip install e621-dl`\n\n## Quickstart\n* To download a post with a given id:  \n`e6 posts get 12345`  \n* To download all posts that match the canine but not 3d tags:  \n`e6 posts search "canine 3d"`  \n* To download 500 posts that match the 3d tag:  \n`e6 posts search 3d -m 500`  \n* To download posts that match the 3d tag to directory e621_downloads:  \n`e6 posts search 3d -d e621_downloads`\n* To download all posts that match the 3d tag and replace all post duplicates from the parent directory with symlinks:  \n`e6 posts search 3d -s`  \n* To download the pool with the given id:  \n`e6 pools get 12345`\n* To replace all post duplicates from the current directory with symlinks:  \n`e6 clean`\n* To save e621 login information to be used for every future query:  \n`e6 login`\n* To remove e621 login information:  \n`e6 logout`\n\nFor advanced reference, use `--help` option. For example, `e6 --help`, `e6 posts search --help`, etc.',
    'author': 'HMiku8338',
    'author_email': 'hmiku8338@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hmiku8338/e621-dl',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
