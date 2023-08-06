# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crontabula']

package_data = \
{'': ['*']}

extras_require = \
{'cli': ['click']}

entry_points = \
{'console_scripts': ['crontabula = crontabula.cli:cli']}

setup_kwargs = {
    'name': 'crontabula',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tom Forbes',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
