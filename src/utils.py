import pandas as pd
from pathlib import Path


def read_datafile(filename: str) -> pd.DataFrame:
    filepath = Path(__file__).parent.parent / "data"
    df = pd.read_csv(filepath / filename)
    return df
