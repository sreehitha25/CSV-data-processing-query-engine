import pandas as pd
import pytest
from src.loader import load_csv

def test_valid_csv(tmp_path):
    p=tmp_path/"a.csv"; pd.DataFrame({"A":[1,2]}).to_csv(p,index=False); assert len(load_csv(p))==2

def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError): load_csv(tmp_path/"missing.csv")

def test_empty_csv(tmp_path):
    p=tmp_path/"empty.csv"; p.write_text("")
    with pytest.raises(ValueError): load_csv(p)
