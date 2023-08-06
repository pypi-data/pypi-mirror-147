# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ggviz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ggviz',
    'version': '0.0.0a0',
    'description': 'ggviz',
    'long_description': '# ggviz\n',
    'author': 'Ryan Munro',
    'author_email': '500774+munro@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/munro/python-ggviz',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
