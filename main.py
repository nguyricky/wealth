from questionary import select, Style
from data import load_or_create_allocations, edit_allocations  # Import the edit_allocations function
from utils import calculate_investment, fetch_stock_prices

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
            print("\nInvestment Allocation:")
            for stock, amount in investment_per_stock.items():
                print(f"{stock}: ${amount:.2f}")
            print("\n")
        elif choice == 'Fetch Portfolio Stock Prices':
            prices = fetch_stock_prices(allocations)
            print("\nCurrent Tracked Stock Prices:")
            for stock, price in prices.items():
                print(f"{stock}: ${price:.2f}")
            print("\n")
        elif choice == 'Edit Portfolio Allocations':
            edit_allocations(filename)
            allocations = load_or_create_allocations(filename)
        elif choice == 'Exit':
            break

if __name__ == "__main__":
    main_menu()
