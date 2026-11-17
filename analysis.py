import numpy as np
import pandas as pd


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


def select_sample(data, countries, start_year, end_year):
    """
    Return the selected countries and inclusive year range.

    Keep country, year, population, GDP and CO2 columns.
    Return a copy without modifying the input DataFrame.
    """
    columns = ["country", "year", "population", "gdp", "co2"]

    return data.loc[
        data["country"].isin(countries)
        & data["year"].between(start_year, end_year),
        columns
    ].copy()

def summarize_growth(data, start_year, end_year):
    """
    Summarize GDP and CO2 percentage changes by country.

    Parameters
    ----------
    data : pandas.DataFrame
        Validated data with country, year, gdp and co2 columns.
        Each country must have one complete record for each
        endpoint year, with positive starting GDP and CO2.
    start_year : int
        Starting year.
    end_year : int
        Ending year, later than start_year.

    Returns
    -------
    pandas.DataFrame
        GDP and CO2 percentage changes and an indicator of
        GDP growth accompanied by lower CO2 emissions.
    """
    start = data.loc[
        data["year"] == start_year
    ].set_index("country")

    end = data.loc[
        data["year"] == end_year
    ].set_index("country")

    summary = pd.DataFrame({
        "gdp_change_pct": percentage_change(start["gdp"], end["gdp"]),
        "co2_change_pct": percentage_change(start["co2"], end["co2"]),
    })

    summary["gdp_up_co2_down"] = (
        (summary["gdp_change_pct"] > 0)
        & (summary["co2_change_pct"] < 0)
    )

    return summary

def add_base_indices(data, base_year):
    """
    Add GDP and CO2 indices relative to a baseline year.

    Parameters
    ----------
    data : pandas.DataFrame
        Data containing country, year, gdp and co2 columns.
    base_year : int
        Baseline year, assigned an index of 100.

    Returns
    -------
    pandas.DataFrame
        A copy with gdp_index and co2_index columns.

    Raises
    ------
    ValueError
        If baseline countries are duplicated, or a required
        baseline value is missing, zero or negative.
    """
    result = data.copy()

    base = data.loc[
        data["year"] == base_year
    ].set_index("country")

    if not base.index.is_unique:
        raise ValueError("Each country must have one baseline record.")

    for column in ["gdp", "co2"]:
        baseline = result["country"].map(base[column])

        if baseline.isna().any() or (baseline <= 0).any():
            raise ValueError(f"Missing or non-positive baseline for {column}.")

        result[f"{column}_index"] = result[column] / baseline * 100

    return result

def add_co2_per_capita(data):
    """Return a copy with annual CO2 emissions in tonnes per person.

    Requires CO2 in million tonnes and population in people.
    Both columns must contain finite values. Population must be
    positive, and CO2 emissions must be non-negative.
    """
    columns = ["co2", "population"]

    if not np.isfinite(data[columns].to_numpy(dtype=float)).all():
        raise ValueError("CO2 and population must contain finite values.")

    if (data["population"] <= 0).any():
        raise ValueError("Population must be greater than zero.")

    if (data["co2"] < 0).any():
        raise ValueError("CO2 emissions must be non-negative.")

    result = data.copy()
    result["co2_per_capita"] = (
        result["co2"] * 1_000_000 / result["population"]
    )

    return result

def add_co2_intensity(data):
    """Return a copy with CO2 intensity in kg per international dollar.

    Requires annual CO2 in million tonnes and GDP in international
    dollars at constant 2011 prices. Both columns must contain
    finite values. GDP must be positive and CO2 non-negative.
    """
    columns = ["co2", "gdp"]

    if not np.isfinite(data[columns].to_numpy(dtype=float)).all():
        raise ValueError("CO2 and GDP must contain finite values.")

    if (data["gdp"] <= 0).any():
        raise ValueError("GDP must be greater than zero.")

    if (data["co2"] < 0).any():
        raise ValueError("CO2 emissions must be non-negative.")

    result = data.copy()
    result["co2_intensity"] = (
        result["co2"] * 1_000_000_000 / result["gdp"]
    )

    return result