from questionary import select, Style
from data.allocations import load_or_create_allocations, edit_allocations, display_portfolio
from utils.fetch import fetch_stock_prices
from utils.calculations import calculate_investment
from utils.csv import display_csv_as_table
from rich.console import Console
from rich.table import Table
from rich.text import Text
from tkinter import filedialog
import tkinter as tk

custom_style = Style([
    ('qmark', ''),
    ('question', 'bold')
])

def main_menu():
    filename = "portfolio_allocations.json"
    allocations = load_or_create_allocations(filename)
    
    console = Console()

    while True:
        choice = select(
            "What do you want to do?",
            choices=[
                'Calculate Investment',
                'Fetch Portfolio Prices',
                'Edit Portfolio Allocations',
                'View Portfolio via CSV',
                'View Current Portfolio Allocations',
                'Exit'
            ],
            style = custom_style
        ).ask()

        if choice == 'Calculate Investment':
            total_investment = float(input("Enter the investment amount: "))
            investment_per_stock = calculate_investment(allocations, total_investment)

            table = Table(show_header=True, header_style = "bold bright_white")
            table.add_column("Stock", style = "sky_blue1")
            table.add_column("Investment Allocation", style = "green4")

            for stock, amount in investment_per_stock.items():
                table.add_row(stock, f"${amount:.2f}")

            console.print(table)
            print("\n")
        
        elif choice == 'Fetch Portfolio Prices':
            stock_data = fetch_stock_prices(allocations)
            table = Table(show_header=True, header_style = "bold bright_white")
            table.add_column("Stock", style = "sky_blue1")
            table.add_column("Price", style = "green4")
            table.add_column("Change")
            table.add_column("Percent Change", style = "light_sky_blue1")

            for stock, data in stock_data.items():
                if data:
                    change_text = Text(data['change'])
                    if data['change'].startswith('+'):
                        change_text.stylize("green")
                    elif data['change'].startswith('-'):
                        change_text.stylize("red")

                    table.add_row(stock, f"${data['price']}", change_text, data['percent_change'])
                else:
                    table.add_row(stock, "N/A", "N/A", "N/A")
            console.print(table)
            print("\n")
        
        elif choice == 'Edit Portfolio Allocations':
            edit_allocations(filename)
            allocations = load_or_create_allocations(filename)
                 
        elif choice == 'View Portfolio via CSV':
            root = tk.Tk()
            root.withdraw()
            csv_file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
            )
            root.destroy()

            if csv_file_path:
                display_csv_as_table(csv_file_path)
            else:
                print("No file selected.")
                
            print("\n")
        
        elif choice == 'View Current Portfolio Allocations':
            display_portfolio(allocations)
            
        elif choice == 'Exit':
            break

if __name__ == "__main__":
    main_menu()
