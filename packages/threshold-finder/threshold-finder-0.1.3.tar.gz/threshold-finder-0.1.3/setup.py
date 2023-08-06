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
    'version': '0.1.3',
    'description': 'Finding optimal threshold based on ROC CURVE.',
    'long_description': 'Installation\n============\n\n.. code-block:: bash\n\n    pip install threshold-finder\n\n\nUsage\n=====\n\nFolowing display an usage example.\n\n.. code-block:: python\n\n    >>> from threshold_finder.finder import OptimalThresholdFinder, ThresholdFinder, YoudenThresholdFinder\n    >>> # Example data\n    >>> true_label = pd.Series([1,1,1,0,0,0])\n    >>> predicted_proba = pd.Series([0.9, 0.8, 0.7, 0.72, 0.6, 0.5])\n\n    >>> # Use a specific finder directly ...\n    >>> finder = YoudenThresholdFinder()\n    >>> optimal_threshold = finder.optimal_threshold(true_label, predicted_proba)\n    >>> print(optimal_threshold)\n    0.7\n\n    >>> # ... Or use the factory\n    >>> factory = ThresholdFinder()\n    >>> finder = factory.get_finder(method="youden_statistic")\n    >>> optimal_threshold = finder.optimal_threshold(true_label, predicted_proba)\n    >>> print(optimal_threshold)\n    0.7\n',
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
