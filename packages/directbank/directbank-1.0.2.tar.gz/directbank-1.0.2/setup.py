# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['directbank', 'directbank.models', 'directbank.views']

package_data = \
{'': ['*']}

install_requires = \
['xsdata==22.4']

setup_kwargs = {
    'name': 'directbank',
    'version': '1.0.2',
    'description': '',
    'long_description': '# directbank\n### Test\n\n![PyPI - Downloads](https://img.shields.io/pypi/dm/directbank)',
    'author': 'Toony',
    'author_email': 'kizyanov@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kizyanov/directbank',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
