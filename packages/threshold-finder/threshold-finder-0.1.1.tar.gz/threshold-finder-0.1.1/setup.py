# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['threshold_finder']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3,<2.0', 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'threshold-finder',
    'version': '0.1.1',
    'description': 'Finding optimal threshold based on ROC CURVE.',
    'long_description': None,
    'author': 'thibaultbl',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
