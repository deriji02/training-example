import pandas as pd
from pathlib import Path
from typing import Any
import csv


def read_datafile(filename: str) -> pd.DataFrame:
    filepath = Path(__file__).parent.parent / "data" / f"{filename}.csv"
    df = pd.read_csv(filepath)
    return df


def csv_read_datafile(filename: str) -> list[list[Any]]:
    filepath = Path(__file__).parent.parent / "data" / f"{filename}.csv"
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        rows = [x for x in reader]
        return rows
