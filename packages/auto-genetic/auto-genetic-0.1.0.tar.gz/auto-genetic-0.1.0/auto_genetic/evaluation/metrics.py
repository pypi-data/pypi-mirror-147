import numpy as np
import pandas as pd


def root_mean_squared_error(error: pd.Series) -> float:
    """
    Function to calculate the rmse of a pd series
    Parameters
    ----------
    error: pd.Series
           pandas series that contains the errors for the model

    Returns
    -------
    float
    the rmse for the specific chromosome we are analysing

    """
    return np.sqrt((error ** 2).mean())


def mean_absolute_error(error: pd.Series) -> float:
    """
    Function to calculate the mae of a pd series
    Parameters
    ----------
    error: pd.Series
          pandas series that contains the errors for the model

    Returns
    -------
    float
    the mae for the specific chromosome we are analysing

    """
    return abs(error).mean()


def symmetric_mean_average_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    """
    Function to calculate the smape of a pd series
    Parameters
    ----------
    y_true: pd.Series
            pandas series that contains the true values for the test set
    y_pred: pd.Series
            pandas series that contains the predicted values for the test set

    Returns
    -------
    float
    the smape for the specific chromosome we are analysing

    """
    errors = 2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred)) * 100
    return errors.mean()


def mean_arctangent_absolute_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    """
    Function to calculate the maape of a pd series
    Parameters
    ----------
    y_true: pd.Series
            pandas series that contains the true values for the test set
    y_pred: pd.Series
            pandas series that contains the predicted values for the test set

    Returns
    -------
    float
    the maape for the specific chromosome we are analysing

    """
    aape = np.arctan(abs((y_true - y_pred) / y_true))
    return aape.mean()
