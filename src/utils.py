"""Small validation helpers."""
def require_number(value: str) -> int:
    try:
        number=int(value)
    except ValueError:
        raise ValueError("Please enter a valid number.")
    if number < 1: raise ValueError("Number must be greater than 0.")
    return number

def get_column(df, column):
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist.")
    return column
