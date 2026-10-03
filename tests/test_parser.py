import pytest
from src.parser import parse_command

def test_load(): assert parse_command("LOAD data/x.csv").args["file"]=="data/x.csv"
def test_filter(): assert parse_command("FILTER Sales > 1000").args=={"column":"Sales","operator":">","value":"1000"}
def test_sort(): assert parse_command("SORT Sales DESC").args["order"]=="DESC"
def test_groupby(): assert parse_command("GROUPBY Region SUM Sales").args["operation"]=="SUM"
def test_invalid():
    with pytest.raises(ValueError): parse_command("WRONG")
