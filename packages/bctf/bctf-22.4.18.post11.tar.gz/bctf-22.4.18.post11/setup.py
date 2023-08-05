# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bctf']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bctf = bctf.main:main']}

setup_kwargs = {
    'name': 'bctf',
    'version': '22.4.18.post11',
    'description': '(WIP) Run own commands before commit / push etc',
    'long_description': '# bctf\n',
    'author': 'Tadeusz Miszczyk',
    'author_email': '42252259+8tm@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
