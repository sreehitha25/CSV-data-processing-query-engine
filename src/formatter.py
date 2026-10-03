"""Output formatting helpers."""
import pandas as pd
try:
    from tabulate import tabulate
except ImportError:
    tabulate=None

def format_table(value) -> str:
    if isinstance(value, pd.Series):
        value=value.to_frame()
    if isinstance(value, pd.DataFrame):
        if value.empty: return "(No rows)"
        if tabulate:
            return tabulate(value, headers="keys", tablefmt="simple", showindex=False)
        return value.to_string(index=False)
    return str(value)
