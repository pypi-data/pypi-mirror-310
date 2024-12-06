"""Scoring functions for model testing"""

import numpy as np
from sklearn.metrics import make_scorer, root_mean_squared_error
from sklearn.model_selection import cross_validate


def maximum_absolute_error(y_true, y_pred):
    """Scoring function for the maximum absolute error

    :parameters:
    y_true: 1-D data structure
      True values of the target variable
    y_pred: 1-D data structure
      Predicted values of the target variable

    :returns:
    Maximum absolute error
    """
    return np.max(np.abs(y_pred - y_true))


def cross_validation(model, x, y):
    """Runs 10-fold cross validation to generate mean-squared error
    and maximum absolute error scores

    :parameters:
    model: sklearn model object
      Model for testing
    x: 2-D data structure
      Input covariates
    y: 1-D data structure
      Target variable

    :returns:
    Mean-squared error and maximum absolute error computed via cross validation
    """
    rmse = make_scorer(root_mean_squared_error)
    max_ae = make_scorer(maximum_absolute_error)
    scores = cross_validate(
        model,
        x,
        y,
        scoring={"mse": rmse, "max_ae": max_ae},
        cv=10,
        return_estimator=True,
    )
    return scores["test_mse"].mean(), scores["test_max_ae"].mean()
