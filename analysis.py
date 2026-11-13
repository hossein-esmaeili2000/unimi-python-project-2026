import numpy as np


def percentage_change(start_value, end_value):
    """
    Calculate percentage change between starting and ending values.

    Parameters
    ----------
    start_value : number or pandas.Series
        Positive starting value(s). For Series inputs, country
        labels must match those in end_value.
    end_value : number or pandas.Series
        Ending value(s), measured in the same units as start_value.

    Returns
    -------
    number or pandas.Series
        Percentage change. Negative values indicate a decrease.

    Raises
    ------
    ValueError
        If any starting value is zero or negative.
    """
    if np.any(start_value <= 0):
        raise ValueError("Starting values must be greater than zero.")

    return (end_value - start_value) / start_value * 100