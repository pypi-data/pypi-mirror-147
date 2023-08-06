Installation
============

.. code-block:: bash

    pip install threshold-finder


Usage
=====

Folowing display an usage example.

.. code-block:: python

    >>> from threshold_finder.finder import OptimalThresholdFinder, ThresholdFinder, YoudenThresholdFinder
    >>> # Example data
    >>> true_label = pd.Series([1,1,1,0,0,0])
    >>> predicted_proba = pd.Series([0.9, 0.8, 0.7, 0.72, 0.6, 0.5])

    >>> # Use a specific finder directly ...
    >>> finder = YoudenThresholdFinder()
    >>> optimal_threshold = finder.optimal_threshold(true_label, predicted_proba)
    >>> print(optimal_threshold)
    0.7

    >>> # ... Or use the factory
    >>> factory = ThresholdFinder()
    >>> finder = factory.get_finder(method="youden_statistic")
    >>> optimal_threshold = finder.optimal_threshold(true_label, predicted_proba)
    >>> print(optimal_threshold)
    0.7
