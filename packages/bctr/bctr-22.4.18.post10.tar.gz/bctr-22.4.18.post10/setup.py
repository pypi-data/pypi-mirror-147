# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bctr']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bctr = bctr.main:main']}

setup_kwargs = {
    'name': 'bctr',
    'version': '22.4.18.post10',
    'description': '(WIP) Run own commands before commit / push etc',
    'long_description': '# bctr\n',
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
