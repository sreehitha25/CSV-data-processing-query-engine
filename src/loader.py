"""CSV loading utilities."""
from pathlib import Path
import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    path=Path(file_path)
    if not path.exists(): raise FileNotFoundError(f"File not found: {file_path}")
    if path.suffix.lower() != ".csv": raise ValueError("Please provide a CSV file.")
    try: df=pd.read_csv(path)
    except pd.errors.EmptyDataError: raise ValueError("The CSV file is empty.")
    except Exception as exc: raise ValueError(f"Invalid CSV file: {exc}")
    if df.empty and len(df.columns)==0: raise ValueError("The CSV file is empty.")
    if len(df.columns)==0: raise ValueError("The CSV file has no columns.")
    return df
