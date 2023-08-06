# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncal']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.1,<2.0.0',
 'google-api-python-client>=2.36.0,<3.0.0',
 'google-auth-oauthlib>=0.4.6,<0.6.0',
 'notion-client>=0.9.0,<0.10.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.21.0',
 'tomli>=2.0.0,<3.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ncal = ncal.cli:app']}

setup_kwargs = {
    'name': 'ncal',
    'version': '0.3.0',
    'description': '',
    'long_description': '[![CodeQL](https://github.com/SG60/ncal/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/SG60/ncal/actions/workflows/codeql-analysis.yml)\n[![Package Tests](https://github.com/SG60/ncal/actions/workflows/tests.yml/badge.svg)](https://github.com/SG60/ncal/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/SG60/ncal/branch/main/graph/badge.svg?token=UZCOEA0YWQ)](https://codecov.io/gh/SG60/ncal)\n[![Code Style](https://github.com/SG60/ncal/actions/workflows/code-style.yml/badge.svg)](https://github.com/SG60/ncal/actions/workflows/code-style.yml)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=SG60_ncal&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=SG60_ncal)\n  \n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ncal?label=supported%20python)](https://pypi.org/project/ncal/)\n[![PyPI](https://img.shields.io/pypi/v/ncal?logo=python)](https://pypi.org/project/ncal/)\n[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/sg60/ncal?label=docker&logo=docker)](https://hub.docker.com/r/sg60/ncal)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# 2-Way Sync for Notion and Google Calendar\n  \nCurrently reworking the documentation.\n\nInstall with `pip install ncal`. This will install the `ncal` command.\n\n## Configuration\nConfiguration is via toml, command line flags, or environment variables (including via a .env file).\n\nConfiguration is via toml, command line flags, or environment variables (including via a .env file). Reading through `config.py` will give a lot of useful information on options. Run `ncal --help` to get more info on the cli command.\n\n## Key dependencies\n- [Notion API Python SDK](https://github.com/ramnes/notion-sdk-py)\n- https://github.com/googleapis/google-api-python-client\n- [Arrow](https://github.com/arrow-py/arrow) for datetime handling\n- Dev:\n  - https://github.com/HypothesisWorks/hypothesis\n  - https://github.com/python/mypy\n',
    'author': 'Sam Greening',
    'author_email': 'samjg60@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sg60.github.io/ncal/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
