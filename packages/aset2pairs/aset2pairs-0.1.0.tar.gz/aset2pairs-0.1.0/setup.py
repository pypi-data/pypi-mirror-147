# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aset2pairs']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'aset2pairs',
    'version': '0.1.0',
    'description': 'Convert aset to block pairs',
    'long_description': '# aset2pairs\n[![pytest](https://github.com/ffreemt/aset2pairs/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/aset2pairs/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/aset2pairs.svg)](https://badge.fury.io/py/aset2pairs)\n\nConvert aset to block pairs\n\n## Install it\n\n```shell\npip install aset2pairs\n# poetry add aset2pairs\n# git clone https://github.com/ffreemt/aset2pairs && cd aset2pairs\n```\n\n## Use it\n```python\nfrom aset2pairs import aset2pairs\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/aset2pairs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
