# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvizbee']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.4.2,<3.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'cmat2aset==0.1.0a7',
 'environs>=9.5.0,<10.0.0',
 'fast-scores==0.1.3a4',
 'icecream>=2.1.2,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'logzero>=1.7.0,<2.0.0',
 'nltk>=3.7,<4.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'panel>=0.12.6,<0.13.0',
 'param>=1.12.0,<2.0.0',
 'seg-text>=0.1.1,<0.2.0',
 'unsync>=1.4.0,<2.0.0']

extras_require = \
{'plot': ['holoviews>=1.14.8,<2.0.0',
          'plotly>=5.6.0,<6.0.0',
          'seaborn>=0.11.2,<0.12.0']}

setup_kwargs = {
    'name': 'pyvizbee',
    'version': '0.1.0a4',
    'description': 'a dualtext alingner based on holoviz panel',
    'long_description': '# pyvizbee\n[![pytest](https://github.com/ffreemt/vizbee/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/vizbee/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/pyvizbee.svg)](https://badge.fury.io/py/pyvizbee)\n\na dualtext aligner based on holoviz panel, currently for English and Chinese texts only\n\n## Python version\nPython 3.8 only, best with python 3.8.3 or 3.8.5\n\n## Install it\n\n```shell\npip install pyvizbee\npython -m pyvizbee\n\n```\n#### Extra\nPlotting is optinal and can be installed with\n```shell\npip install pyvizbee[plot]\n```\nor simply install the required packages (holoviews,\nplotly, seaborn), e.g. `pip install holoviews\nplotly seaborn`\n\n### Post-install\nSince `polyglot` is needed but presents some problems with dicrect pip/poetry install method, a manual installation step is required.\n\n* Linux and friends: `pip install polyglot`\n\n* Windows: download and install whl for pyicu and pycld2\n    * `pip install git+https://github.com/aboSamoor/polyglot@master`\n\n## Use it\n```shell\npython -m pyvizbee\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/vizbee',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
