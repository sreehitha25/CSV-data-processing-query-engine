# CSV Data Processing Query Engine

## Overview
A small Python command-line tool for loading CSV files and running common data operations without writing Pandas code manually.

## Problem Statement
CSV files are easy to create but repetitive filtering, sorting and aggregation normally require code. This project provides a simple query-style interface for those operations.

## Objective
Build a student-friendly CLI that demonstrates Python, Pandas, OOP, DSA-style command parsing and SQL-like query concepts.

## Features
- Load and inspect CSV data
- Filter, search, sort and select columns
- Count and find unique values
- Numeric summaries and GROUPBY aggregation
- TOP values and CSV export
- Input validation and error handling

## Technologies
Python 3.10+, Pandas, Pytest, standard library, optional tabulate.

## How it works
The parser converts a typed command into a small structured object. The QueryEngine validates the request and performs the operation on a Pandas DataFrame. Results are formatted for the terminal or exported to CSV.

## Architecture
`User -> Command Parser -> QueryEngine -> Pandas DataFrame -> Terminal/CSV`

## Project Structure
```text
main.py
src/ (parser, loader, executor, formatter, utils)
data/sample_sales.csv
output/.gitkeep
tests/
```

## Installation
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Running
```bash
python main.py
```

## Example Commands
```text
LOAD data/sample_sales.csv
SHOW
HEAD 5
FILTER Sales > 1000
SORT Sales DESC
GROUPBY Region SUM Sales
TOP 5 Sales
EXPORT output/result.csv
RESET
EXIT
```

## Testing
```bash
pytest -q
```

## Limitations
The parser is intentionally simple. Commands use whitespace-separated arguments, CSV is the only supported file type, and GROUPBY numeric operations require a numeric target column.

## Future Improvements
Quoted values containing spaces, more date operations, pagination for large datasets, and additional aggregation functions could be added.

## Resume Description
Built a Python-based CSV query engine to load, filter, sort, search, aggregate, and export structured datasets through a command-line interface. Implemented a custom command parser and query execution layer with validation, using Pandas DataFrames and Pytest for core testing.
