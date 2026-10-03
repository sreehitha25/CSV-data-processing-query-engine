import pandas as pd
import pytest
from src.parser import parse_command
from src.executor import QueryEngine

@pytest.fixture
def engine(tmp_path):
    p=tmp_path/"data.csv"; pd.DataFrame({"Region":["West","East","West"],"Sales":[1500,700,500],"Product":["Laptop","Chair","Laptop"]}).to_csv(p,index=False)
    e=QueryEngine(); e.execute(parse_command(f"LOAD {p}")); return e

def test_filter(engine): assert len(engine.execute(parse_command("FILTER Sales > 1000")))==1
def test_sort(engine): assert engine.execute(parse_command("SORT Sales DESC")).iloc[0]["Sales"]==1500
def test_select(engine): assert list(engine.execute(parse_command("SELECT Region, Sales")).columns)==["Region","Sales"]
def test_count(engine): assert engine.execute(parse_command("COUNT"))==3
def test_groupby(engine): assert engine.execute(parse_command("GROUPBY Region SUM Sales")).set_index("Region").loc["West","SUM"]==2000
def test_summary(engine): assert "mean" in engine.execute(parse_command("SUMMARY Sales")).index
def test_reset(engine): engine.execute(parse_command("RESET")); assert engine.data is None
