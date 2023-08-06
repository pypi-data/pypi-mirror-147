# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytocode']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytocode',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kyle Oliver',
    'author_email': 'oliverke@mail.uc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
