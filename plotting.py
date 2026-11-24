from pathlib import Path

import matplotlib.pyplot as plt

def plot_country_trends(data, countries, base_year):
    """
    Display and save GDP and CO2 index charts by country.

    Parameters
    ----------
    data : pandas.DataFrame
        Data with country, year, gdp_index and co2_index columns.
        Indices must already use the specified base_year.
    countries : list of str
        Countries to plot.
    base_year : int
        Baseline year used to calculate the indices.

    Returns
    -------
    list of pathlib.Path
        Paths of the saved PNG files.
    """
    output_directory = (
        Path(__file__).resolve().parent / "outputs" / "figures"
    )
    output_directory.mkdir(parents=True, exist_ok=True)

    saved_paths = []

    for country in countries:
        country_data = data.loc[
            data["country"] == country
        ].sort_values("year")

        if country_data.empty:
            raise ValueError(f"No data available for {country}.")

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.plot(country_data["year"], country_data["gdp_index"], label="GDP")
        ax.plot(country_data["year"], country_data["co2_index"], label="CO2")
        ax.axhline(100, color="gray", linestyle="--", linewidth=1)

        first_year = country_data["year"].min()
        last_year = country_data["year"].max()

        ax.set_title(
            f"{country}: GDP and CO2 emissions, {first_year}–{last_year}"
        )
        ax.set_xlabel("Year")
        ax.set_ylabel(f"Index ({base_year} = 100)")
        ax.legend()
        ax.grid(alpha=0.3)

        fig.tight_layout()

        filename = country.lower().replace(" ", "_") + "_gdp_co2_index.png"
        figure_path = output_directory / filename

        fig.savefig(figure_path, dpi=300, bbox_inches="tight")
        saved_paths.append(figure_path)

        plt.show()
        plt.close(fig)

    return saved_paths


def plot_co2_per_capita(data, countries):
    """Plot annual CO2 emissions in tonnes per person.

    Requires country, year and co2_per_capita columns.
    Save the chart and return its Path.
    """
    output_directory = (
        Path(__file__).resolve().parent / "outputs" / "figures"
    )
    output_directory.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    for country in countries:
        country_data = data.loc[
            data["country"] == country
        ].sort_values("year")

        ax.plot(
            country_data["year"],
            country_data["co2_per_capita"],
            label=country
        )

    first_year = data.loc[
        data["country"].isin(countries), "year"
    ].min()
    last_year = data.loc[
        data["country"].isin(countries), "year"
    ].max()

    ax.set_title(
        f"CO2 emissions per capita, {first_year}–{last_year}"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("CO2 emissions (tonnes per person per year)")
    ax.set_ylim(bottom=0)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()

    figure_path = output_directory / "co2_per_capita_comparison.png"
    fig.savefig(figure_path, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close(fig)

    return figure_path

def plot_co2_intensity(data, countries):
    """Plot CO2 intensity in kg per international dollar of GDP.

    GDP is measured at constant 2011 prices.
    Save the comparison chart and return its Path.
    """
    selected = data.loc[data["country"].isin(countries)]

    if selected.empty:
        raise ValueError("No data found for the selected countries.")

    for country in countries:
        if not selected["country"].eq(country).any():
            raise ValueError(f"No data found for {country}.")

    output_directory = (
        Path(__file__).resolve().parent / "outputs" / "figures"
    )
    output_directory.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    for country in countries:
        country_data = selected.loc[
            selected["country"] == country
        ].sort_values("year")

        ax.plot(
            country_data["year"],
            country_data["co2_intensity"],
            label=country
        )

    first_year = selected["year"].min()
    last_year = selected["year"].max()

    ax.set_title(f"CO2 intensity of GDP, {first_year}–{last_year}")
    ax.set_xlabel("Year")
    ax.set_ylabel("CO2 (kg per international $ of GDP, 2011 prices)")
    ax.set_ylim(bottom=0)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()

    figure_path = output_directory / "co2_intensity_comparison.png"
    fig.savefig(figure_path, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close(fig)

    return figure_path