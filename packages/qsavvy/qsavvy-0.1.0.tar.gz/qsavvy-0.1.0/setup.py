# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qsavvy', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click==8.0.1']

extras_require = \
{'dev': ['black>=21.5b2,<22.0',
         'mypy>=0.900,<0.901',
         'tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'mkdocs>=1.1.2,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

entry_points = \
{'console_scripts': ['qsavvy = qsavvy.cli:main']}

setup_kwargs = {
    'name': 'qsavvy',
    'version': '0.1.0',
    'description': "savvy's Quantum Stuff.",
    'long_description': "# Qsavvy\n\n\n[![pypi](https://img.shields.io/pypi/v/qsavvy.svg)](https://pypi.org/project/qsavvy/)\n[![python](https://img.shields.io/pypi/pyversions/qsavvy.svg)](https://pypi.org/project/qsavvy/)\n[![Build Status](https://github.com/anomius/qsavvy/actions/workflows/dev.yml/badge.svg)](https://github.com/anomius/qsavvy/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/anomius/qsavvy/branch/main/graphs/badge.svg)](https://codecov.io/github/anomius/qsavvy)\n\n\n\nsavvy's Quantum Stuff\n\n\n* Documentation: <https://anomius.github.io/qsavvy>\n* GitHub: <https://github.com/anomius/qsavvy>\n* PyPI: <https://pypi.org/project/qsavvy/>\n* Free software: BSD-3-Clause\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n",
    'author': 'Swaraj Purohit',
    'author_email': 'swarajpurohit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anomius/qsavvy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
