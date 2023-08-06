# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ppw']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter==1.7.2']

extras_require = \
{'dev': ['pytest>=5.4.3,<6.0.0',
         'pytest-cookies>=0.5.1,<0.6.0',
         'pyyaml>=5.3.1,<6.0.0',
         'mkdocs>=1.1.2,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocs-material-extensions>=1.0.1,<2.0.0',
         'pytest-cov>=2.10.1,<3.0.0',
         'tox>=3.20.1,<4.0.0',
         'mkdocs-include-markdown-plugin>=2.8.0,<3.0.0',
         'fire>=0.4.0,<0.5.0']}

entry_points = \
{'console_scripts': ['ppw = ppw.cli:main']}

setup_kwargs = {
    'name': 'ppw',
    'version': '1.1.1',
    'description': 'A Wizard to create a skeleton python project with up-to-date technology',
    'long_description': "# Python Project Wizard\n\nA tool for creating skeleton python project, built with popular develop tools and\nconform to best practice.\n\n[![Version](http://img.shields.io/pypi/v/ppw?color=brightgreen)](https://pypi.python.org/pypi/ppw)\n[![CI Status](https://github.com/zillionare/python-project-wizard/actions/workflows/release.yml/badge.svg)](https://github.com/zillionare/python-project-wizard)\n[![Dowloads](https://img.shields.io/pypi/dm/ppw)](https://pypi.org/project/ppw/)\n[![License](https://img.shields.io/pypi/l/ppw)](https://opensource.org/licenses/BSD-2-Clause)\n![Python Versions](https://img.shields.io/pypi/pyversions/ppw)\n\n\n## Features\n\nThis tool will create Python project with the following features:\n\n* [Poetry]: Manage version, dependancy, build and release\n* [Mkdocs]: Writting your docs in markdown style\n* Testing with [Pytest] (unittest is still supported out of the box)\n* Code coverage report and endorsed by [Codecov]\n* [Tox]: Test your code against environment matrix, lint and artifact check.\n* Format with [Black] and [Isort]\n* Lint code with [Flake8] and [Flake8-docstrings]\n* [Pre-commit hooks]: Formatting/linting anytime when commit/run local tox/CI\n* [Mkdocstrings]: Auto API doc generation\n* Command line interface using [Python Fire] (optional)\n* Continuouse Integration/Deployment by [github actions], includes:\n    - publish dev build/official release to TestPyPI/PyPI automatically when CI success\n    - publish documents automatically when CI success\n    - extract change log from github and integrate with release notes automatically\n* Host your documentation from [Git Pages] with zero-config\n\n## Quickstart\n\nInstall ppw if you haven't install it yet:\n\n```\n  pip install -U ppw\n```\n\nGenerate a Python package project by simple run:\n\n```\n  ppw\n```\n\nThen follow **[Tutorial](https://zillionare.github.io/python-project-wizard/tutorial/)** to finish other configurations.\n\n# Credits\n\nThis repo is forked from [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage), and borrowed some ideas from [briggySmalls](https://github.com/briggySmalls/cookiecutter-pypackage)\n\n\n[poetry]: https://python-poetry.org/\n[mkdocs]: https://www.mkdocs.org\n[pytest]: https://pytest.org\n[codecov]: https://codecov.io\n[tox]: https://tox.readthedocs.io\n[black]: https://github.com/psf/black\n[isort]: https://github.com/PyCQA/isort\n[flake8]: https://flake8.pycqa.org\n[flake8-docstrings]: https://pypi.org/project/flake8-docstrings/\n[mkdocstrings]: https://mkdocstrings.github.io/\n[Python Fire]: https://github.com/google/python-fire\n[github actions]: https://github.com/features/actions\n[Git Pages]: https://pages.github.com\n[Pre-commit hooks]: https://pre-commit.com/\n\n# More projects by same author\n## cfg4py\n[cfg4py](https://pypi.org/project/cfg4py/) is a great tool for managing configuration files, supporting configuration for different environments (dev, prodction and test), automatically converting yaml-based configuration to python class, so you can access configuration items by attribute, thus enable auto-completion (by IDE). It also support live-reload, remote central configuration, config template and more.\n",
    'author': 'Aaron Yang',
    'author_email': 'aaron_yang@jieyu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zillionare/cookiecutter-pypackage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
