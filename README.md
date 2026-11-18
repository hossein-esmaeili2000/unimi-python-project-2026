# Green Growth: Economic Growth and CO₂ Emissions

Python module project for **Coding for Data Science and Data Management**, University of Milan, academic year 2026/27.

**Author:** Hossein Esmaeili  
**Status:** Work in progress

## Research question

Between 1990 and 2022, which selected countries increased their GDP while reducing annual CO₂ emissions?

The analysis compares **Italy, Germany, the United States, China and India**, using endpoint percentage changes and annual indices with **1990 = 100**.

## Data

Source: [Our World in Data CO₂ dataset](https://github.com/owid/co2-data).

The notebook downloads the dataset and its codebook from a fixed repository revision:

`22d9a01321ddec951b36f2bfc66e05dc6ad50ad8`

Files are saved in `data/raw/`. Download metadata, file sizes and SHA-256 hashes are recorded in `data/raw/sources.json`.

Raw CSV files are excluded from Git. The notebook downloads them when they are absent.

Indicators:

- **GDP:** total annual economic output, adjusted for inflation and differences in living costs; international dollars at 2011 prices.
- **CO₂:** annual total emissions excluding land-use change; million tonnes.
- **Population:** number of people.

## Project structure

| File or directory | Purpose |
|---|---|
| `green_growth.ipynb` | Analysis narrative, function calls, tables and charts |
| `data_io.py` | Project paths, snapshot downloads, CSV checks and data loading |
| `analysis.py` | Sample selection, percentage changes, growth summaries and baseline indices |
| `plotting.py` | Display and save country-level GDP and CO₂ index charts |
| `data/raw/` | Downloaded CSV files and source metadata |
| `outputs/figures/` | Generated PNG charts |
| `requirements.txt` | Required package versions |

## Setup and execution

Validated on Windows with Python 3.14.7 using a fresh clone and a newly created virtual environment. Dependencies were installed from requirements.txt, both raw CSV files were downloaded automatically, and all notebook cells completed without errors, displaying all five country charts. This check was performed on the author's computer; other operating systems have not been tested.

1. Clone the repository:

```bash
git clone https://github.com/hossein-esmaeili2000/unimi-python-project-2026.git
cd unimi-python-project-2026
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Install dependencies using the environment's Python.

Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

4. Open the project folder in VS Code with the Python and Jupyter extensions installed.
5. Open `green_growth.ipynb` and select the `.venv` Python kernel.
6. Run all cells from top to bottom.

Internet access is required for dependency installation and the initial data download. Subsequent data loading uses the local files.

## Key findings

- From 1990 to 2022, GDP grew and total CO₂ emissions fell in
  Germany, Italy, and the United States (absolute decoupling).
  In China and India, emissions rose more slowly than GDP
  (relative decoupling).
- CO₂ emissions per unit of GDP fell in all five countries.
  The United States had the highest per-capita emissions among
  the five in 2022, at 14.83 tonnes per person.
- The absolute-decoupling classification was consistent across
  the three start years tested (1990, 2000, and 2010), with 2022
  as the common end year. The size of the emissions changes
  varied across periods.

See section 13 of [the notebook](green_growth.ipynb) for the
full results and limitations.

## Outputs
Five country charts compare GDP and CO₂ indices (1990 = 100).

Two additional charts compare the five countries on shared scales:
- Annual CO₂ emissions per capita, in tonnes per person per year.
- CO₂ intensity of GDP, in kilograms per international dollar
  at constant 2011 prices.

All seven charts are saved as PNG files in `outputs/figures/`.

The notebook also exports two tables:

- [GDP and total CO₂ changes, 1990–2022](outputs/tables/growth_1990_2022.csv)
- [Absolute decoupling across the three periods](outputs/tables/decoupling_by_period.csv)

## Limitations

- Countries were selected purposefully; results do not represent all countries.
- The analysis describes associations and does not establish causation.
- CO₂ excludes land-use change and does not represent all greenhouse gases.
- Endpoint classifications may change with the selected period.
- Indices compare relative changes, not absolute economic or emissions levels.
- Separate charts use different vertical scales.
- The project uses a fixed data snapshot rather than an automatically updated dataset.

## Next steps

Improve notebook explanations, organize reusable analysis code into modules, check sensitivity to the selected period, and practise explaining the implementation and findings.
