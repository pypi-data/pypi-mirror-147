# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kilbourn_modern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.15.0,<4.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['modern-python = kilbourn_modern_python.console:main']}

setup_kwargs = {
    'name': 'kilbourn-modern-python',
    'version': '0.1.0',
    'description': 'The hypermodern Python Project',
    'long_description': '[![Tests](https://github.com/stephenkilbourn/modern-python/workflows/Tests/badge.svg)](https://github.com/stephenkilbourn/modern-python/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/stephenkilbourn/modern-python/branch/main/graph/badge.svg?token=BVRCL8CZZB)](https://codecov.io/gh/stephenkilbourn/modern-python)\n[![PyPI](https://img.shields.io/pypi/v/modern-python.svg)](https://pypi.org/project/modern-python/)\n\n\n\n\n# modern-python\nworking through [hypermodern-python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)\n',
    'author': 'Stephen Kilbourn',
    'author_email': 'stephenkilbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephenkilbourn/hypermodern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
