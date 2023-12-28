from questionary import select, Style
from data import load_or_create_allocations, edit_allocations
from utils import calculate_investment, fetch_stock_prices
from tabulate import tabulate

custom_style = Style([
    ('qmark', ''),
    ('question', 'bold')
])

def main_menu():
    filename = "portfolio_allocations.json"
    allocations = load_or_create_allocations(filename)

    while True:
        choice = select(
            "What do you want to do?",
            choices=[
                'Calculate Investment',
                'Fetch Portfolio Stock Prices',
                'Edit Portfolio Allocations',
                'Exit'
            ],
            style=custom_style
        ).ask()

        if choice == 'Calculate Investment':
            total_investment = float(input("Enter the investment amount: "))
            investment_per_stock = calculate_investment(allocations, total_investment)

            table_data = [[stock, f"${amount:.2f}"] for stock, amount in investment_per_stock.items()]

            print("\nInvestment Allocation:")
            print(tabulate(table_data, headers=["Stock", "Investment Amount"]))
            print("\n")
        elif choice == 'Fetch Portfolio Stock Prices':
            stock_data = fetch_stock_prices(allocations)
            table_data = []

            for stock, data in stock_data.items():
                if data:
                    table_data.append([stock, f"${data['price']}", data['change'], data['percent_change']])
                else:
                    table_data.append([stock, "N/A", "N/A", "N/A"])

            print("\nCurrent Tracked Stock Prices:\n")
            print(tabulate(table_data, headers=["Stock", "Price", "Change", "Percent Change"]))
            print("\n")
        elif choice == 'Edit Portfolio Allocations':
            edit_allocations(filename)
            allocations = load_or_create_allocations(filename)
        elif choice == 'Exit':
            break

if __name__ == "__main__":
    main_menu()
