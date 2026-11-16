from pathlib import Path
from urllib.request import urlopen
from datetime import datetime, timezone

import csv
import hashlib
import json
import shutil

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DIRECTORY = PROJECT_ROOT / "data" / "raw"

SOURCE_REVISION = "22d9a01321ddec951b36f2bfc66e05dc6ad50ad8"
BASE_URL = (
    f"https://raw.githubusercontent.com/owid/co2-data/{SOURCE_REVISION}"
)

SOURCE_FILES = [
    "owid-co2-data.csv",
    "owid-co2-codebook.csv",
]

def validate_csv(file_path, required_columns):
    """
    Check required CSV columns and the first data row.

    Parameters
    ----------
    file_path : pathlib.Path
        CSV file to inspect.
    required_columns : set of str
        Column names that must be present.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the header or first data row is missing or invalid.
    """
    with file_path.open(encoding="utf-8-sig", newline="") as input_file:
        reader = csv.reader(input_file)
        header = next(reader, None)
        first_row = next(reader, None)

    if header is None or first_row is None:
        raise ValueError(f"CSV is empty or has no data rows: {file_path.name}")

    if not required_columns.issubset(header):
        raise ValueError(f"Required columns are missing: {file_path.name}")

    if len(first_row) != len(header):
        raise ValueError(f"Invalid first data row: {file_path.name}")

def download_data():
    """
    Download missing snapshot files and check existing files.

    Returns
    -------
    pathlib.Path
        Directory containing the raw CSV files and source metadata.

    Raises
    ------
    ValueError
        If CSV validation fails, or recorded file identity differs.
    """
    RAW_DIRECTORY.mkdir(parents=True, exist_ok=True)
    manifest_path = RAW_DIRECTORY / "sources.json"

    previous_records = {}
    if manifest_path.exists():
        previous_records = {
            record["filename"]: record
            for record in json.loads(
                manifest_path.read_text(encoding="utf-8")
            )
        }

    records = []

    for filename in SOURCE_FILES:
        destination = RAW_DIRECTORY / filename
        temporary = destination.with_suffix(".csv.part")
        source_url = f"{BASE_URL}/{filename}"
        previous = previous_records.get(filename)
        downloaded = False

        if previous and (
            previous["revision"] != SOURCE_REVISION
            or previous["url"] != source_url
        ):
            raise ValueError(f"Snapshot metadata mismatch: {filename}")

        try:
            if not destination.exists():
                with urlopen(source_url, timeout=60) as response:
                    with temporary.open("wb") as output:
                        shutil.copyfileobj(response, output)

                candidate = temporary
                downloaded = True
            else:
                candidate = destination

            required_columns = (
                {"country", "year", "co2", "gdp", "population"}
                if filename == "owid-co2-data.csv"
                else {"column", "description", "unit"}
            )
            validate_csv(candidate, required_columns)

            digest = hashlib.sha256(candidate.read_bytes()).hexdigest()

            if previous and digest != previous["sha256"]:
                raise ValueError(f"File hash mismatch: {filename}")

            if downloaded:
                temporary.replace(destination)

            retrieved_at = (
                datetime.now(timezone.utc).isoformat()
                if downloaded
                else previous.get("retrieved_at_utc") if previous else None
            )

            records.append({
                "filename": filename,
                "url": source_url,
                "revision": SOURCE_REVISION,
                "retrieved_at_utc": retrieved_at,
                "bytes": destination.stat().st_size,
                "sha256": digest,
            })

            status = "Downloaded" if downloaded else "Verified existing"
            print(f"{status}: {filename}")

        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    manifest_path.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )

    return RAW_DIRECTORY

def load_data():
    """
    Read the local CO2 dataset and its codebook.

    Run download_data before calling this function.

    Returns
    -------
    tuple of pandas.DataFrame
        The main dataset followed by the codebook.

    Raises
    ------
    FileNotFoundError
        If a required CSV file is absent.
    """
    data_path = RAW_DIRECTORY / "owid-co2-data.csv"
    codebook_path = RAW_DIRECTORY / "owid-co2-codebook.csv"

    data = pd.read_csv(data_path)
    codebook = pd.read_csv(codebook_path)

    return data, codebook