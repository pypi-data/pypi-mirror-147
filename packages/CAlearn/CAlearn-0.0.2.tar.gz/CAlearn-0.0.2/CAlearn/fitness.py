"""Metrics to evaluate the fitness of a program.

The :mod:`CAlearn.fitness` module contains some metric with which to evaluate
the computer programs created by the :mod:`CAlearn.genetic` module.
"""

# Author: Trevor Stephens <trevorstephens.com>
# Modified by: Chen Shu <shuchenjp@gmail.com>
#              to add fitness calculation for cellular automaton system.
# License: BSD 3 clause

import numbers

import numpy as np
from joblib import wrap_non_picklable_objects
from scipy.stats import rankdata

__all__ = ['make_fitness']


class _Fitness(object):

    """A metric to measure the fitness of a program.

    This object is able to be called with NumPy vectorized arguments and return
    a resulting floating point score quantifying the quality of the program's
    representation of the true relationship.

    Parameters
    ----------
    function : callable
        A function with signature function(y, y_pred, sample_weight) that
        returns a floating point number. Where `y` is the input target y
        vector, `y_pred` is the predicted values from the genetic program, and
        sample_weight is the sample_weight vector.

    greater_is_better : bool
        Whether a higher value from `function` indicates a better fit. In
        general this would be False for metrics indicating the magnitude of
        the error, and True for metrics indicating the quality of fit.

    """

    def __init__(self, function, greater_is_better):
        self.function = function
        self.greater_is_better = greater_is_better
        self.sign = 1 if greater_is_better else -1

    def __call__(self, *args):
        return self.function(*args)


def make_fitness(function, greater_is_better, wrap=True):
    """Make a fitness measure, a metric scoring the quality of a program's fit.

    This factory function creates a fitness measure object which measures the
    quality of a program's fit and thus its likelihood to undergo genetic
    operations into the next generation. The resulting object is able to be
    called with NumPy vectorized arguments and return a resulting floating
    point score quantifying the quality of the program's representation of the
    true relationship.

    Parameters
    ----------
    function : callable
        A function with signature function(y, y_pred, sample_weight) that
        returns a floating point number. Where `y` is the input target y
        vector, `y_pred` is the predicted values from the genetic program, and
        sample_weight is the sample_weight vector.

    greater_is_better : bool
        Whether a higher value from `function` indicates a better fit. In
        general this would be False for metrics indicating the magnitude of
        the error, and True for metrics indicating the quality of fit.

    wrap : bool, optional (default=True)
        When running in parallel, pickling of custom metrics is not supported
        by Python's default pickler. This option will wrap the function using
        cloudpickle allowing you to pickle your solution, but the evolution may
        run slightly more slowly. If you are running single-threaded in an
        interactive Python session or have no need to save the model, set to
        `False` for faster runs.

    """
    if not isinstance(greater_is_better, bool):
        raise ValueError('greater_is_better must be bool, got %s'
                         % type(greater_is_better))
    if not isinstance(wrap, bool):
        raise ValueError('wrap must be an bool, got %s' % type(wrap))
    if function.__code__.co_argcount != 3:
        raise ValueError('function requires 3 arguments (y, y_pred, w),'
                         ' got %d.' % function.__code__.co_argcount)
    if not isinstance(function(np.array([1, 1]),
                      np.array([2, 2]),
                      np.array([1, 1])), numbers.Number):
        raise ValueError('function must return a numeric.')

    if wrap:
        return _Fitness(function=wrap_non_picklable_objects(function),
                        greater_is_better=greater_is_better)
    return _Fitness(function=function,
                    greater_is_better=greater_is_better)

# _weighted_pearson is disabled in CAlearn due to the diffrences between CA fitness calculation and function fitness calculation.
def _weighted_pearson(y, y_pred, w):
    """Calculate the weighted Pearson correlation coefficient."""
    raise Exception("_weighted_pearson is disabled in CAlearn.")
    with np.errstate(divide='ignore', invalid='ignore'):
        y_pred_demean = y_pred - np.average(y_pred, weights=w)
        y_demean = y - np.average(y, weights=w)
        corr = ((np.sum(w * y_pred_demean * y_demean) / np.sum(w)) /
                np.sqrt((np.sum(w * y_pred_demean ** 2) *
                         np.sum(w * y_demean ** 2)) /
                        (np.sum(w) ** 2)))
    if np.isfinite(corr):
        return np.abs(corr)
    return 0.

# _weighted_spearman is disabled in CAlearn due to the diffrences between CA fitness calculation and function fitness calculation.
def _weighted_spearman(y, y_pred, w):
    """Calculate the weighted Spearman correlation coefficient."""
    raise Exception("_weighted_spearman is disabled in CAlearn.")
    y_pred_ranked = np.apply_along_axis(rankdata, 0, y_pred)
    y_ranked = np.apply_along_axis(rankdata, 0, y)
    return _weighted_pearson(y_pred_ranked, y_ranked, w)

# _mean_absolute_error is disabled in CAlearn due to the diffrences between CA fitness calculation and function fitness calculation.
def _mean_absolute_error(y, y_pred, w):
    """Calculate the mean absolute error."""
    raise Exception("_mean_absolute_error is disabled in CAlearn.")
    return np.average(np.abs(y_pred - y), weights=w)

# _mean_square_error is disabled in CAlearn due to the diffrences between CA fitness calculation and function fitness calculation.
def _mean_square_error(y, y_pred, w):
    """Calculate the mean square error."""
    raise Exception("_mean_square_error is disabled in CAlearn.")
    return np.average(((y_pred - y) ** 2), weights=w)

# _root_mean_square_error is disabled in CAlearn due to the diffrences between CA fitness calculation and function fitness calculation.
def _root_mean_square_error(y, y_pred, w):
    """Calculate the root mean square error."""
    raise Exception("_root_mean_square_error is disabled in CAlearn.")
    return np.sqrt(np.average(((y_pred - y) ** 2), weights=w))

# _log_loss is disabled in CAlearn due to the diffrences between CA fitness calculation and function fitness calculation.
def _log_loss(y, y_pred, w):
    """Calculate the log loss."""
    raise Exception("_log_loss is disabled in CAlearn.")
    eps = 1e-15
    inv_y_pred = np.clip(1 - y_pred, eps, 1 - eps)
    y_pred = np.clip(y_pred, eps, 1 - eps)
    score = y * np.log(y_pred) + (1 - y) * np.log(inv_y_pred)
    return np.average(-score, weights=w)

def _weighted_CAerror(y, y_pred, w):
    """Calculate the error between 2 Cellular Automaton system."""
    if len(y) <= 1:
        raise Exception("_weighted_CAerror: The size of 'y' input in CAerror calculation is less than 1 or equal to 1.")
    if len(y_pred) <= 1:
        raise Exception("_weighted_CAerror: The size of 'y_pred' input in CAerror calculation is less than 1 or equal to 1.")
    if len(y) != len(y_pred):
        raise Exception("_weighted_CAerror: The size of 'y_pred' is not equal to the size of 'y'.")
    if len(y[0]) != len(y_pred[0]):
        raise Exception("_weighted_CAerror: The size of 'y_pred[:]' is not equal to the size of 'y[:]'.")
    total_time_error = 0.0
    for i in range(1, len(y)):
        for j in range(len(y[0])):
            total_time_error += np.absolute(y_pred[i][j] - y[i][j])
    return total_time_error


weighted_pearson = _Fitness(function=_weighted_pearson,
                            greater_is_better=True)
weighted_spearman = _Fitness(function=_weighted_spearman,
                             greater_is_better=True)
mean_absolute_error = _Fitness(function=_mean_absolute_error,
                               greater_is_better=False)
mean_square_error = _Fitness(function=_mean_square_error,
                             greater_is_better=False)
root_mean_square_error = _Fitness(function=_root_mean_square_error,
                                  greater_is_better=False)
log_loss = _Fitness(function=_log_loss,
                    greater_is_better=False)

weighted_CAerror = _Fitness(function=_weighted_CAerror,
                    greater_is_better=False)

_fitness_map = {'pearson': weighted_pearson,
                'spearman': weighted_spearman,
                'mean absolute error': mean_absolute_error,
                'mse': mean_square_error,
                'rmse': root_mean_square_error,
                'log loss': log_loss,
                'CAerror': weighted_CAerror}
