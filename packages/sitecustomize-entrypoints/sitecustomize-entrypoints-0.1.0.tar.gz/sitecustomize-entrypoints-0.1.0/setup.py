# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sitecustomize',
 'sitecustomize._vendor',
 'sitecustomize._vendor.importlib_metadata']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sitecustomize-entrypoints',
    'version': '0.1.0',
    'description': '',
    'long_description': "# sitecustomize-entrypoints\n\nA very simple library that makes a python module called `sitecustomize`\navailable. Python's [site](https://docs.python.org/3/library/site.html)\nmodule gives it, and `usercustomize`, special treatment by importing it after\nit is done looking for and processing .pth files.\n\nWhat this package does is that is finds all `sitecustomize` entry points and,\nif they are callable, calls them.",
    'author': 'Dos Moonen',
    'author_email': 'd.moonen@nki.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Darsstar/sitecustomize-entrypoints',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
