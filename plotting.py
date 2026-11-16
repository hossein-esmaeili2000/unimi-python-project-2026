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