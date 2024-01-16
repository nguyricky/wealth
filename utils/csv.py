import pandas as pd
from rich.table import Table
from rich.console import Console

def display_csv_as_table(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    table = Table(show_header=True, header_style="bold bright_white")
    for column in df.columns:
        table.add_column(str(column))

    for index, row in df.iterrows():
        table.add_row(*[str(item) for item in row])

    console = Console()
    console.print(table)
