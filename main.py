import json
import os
import requests

def get_portfolio_allocations(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_portfolio_allocations(filename, allocations):
    with open(filename, 'w') as file:
        json.dump(allocations, file)

def edit_portfolio_allocations(filename):
    allocations = get_portfolio_allocations(filename)
    print("Editing portfolio allocations. Enter 'done' to finish.")
    while True:
        stock = input("Enter stock name (or 'done' to finish): ")
        if stock.lower() == 'done':
            break
        percentage = float(input(f"Enter allocation percentage for {stock}: "))
        allocations[stock] = percentage
    save_portfolio_allocations(filename, allocations)

def fetch_stock_prices(allocations):
    api_key = 'YOUR_API_KEY'
    prices = {}
    for stock in allocations.keys():
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        price = data["Global Quote"]["05. price"]
        prices[stock] = float(price)
    return prices


def calculate_investment(allocations, total_investment):
    investment_per_stock = {}
    for stock, percentage in allocations.items():
        investment_per_stock[stock] = total_investment * (percentage / 100)
    return investment_per_stock

def main_menu():
    filename = "portfolio_allocations.json"
    while True:
        print("\n--- Menu ---\n")
        print("1. Enter total investment amount")
        print("2. Fetch current stock prices")
        print("3. Edit portfolio allocations")
        print("4. Exit")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            total_investment = float(input("Enter the total investment amount: "))
            allocations = get_portfolio_allocations(filename)
            investment_per_stock = calculate_investment(allocations, total_investment)
            
            print("\nInvestment Allocation:")
            for stock, amount in investment_per_stock.items():
                print(f"{stock}: ${amount:.2f}")
        elif choice == '2':
            allocations = get_portfolio_allocations(filename)
            prices = fetch_stock_prices(allocations)
            print("\nCurrent Stock Prices:", prices)
        elif choice == '3':
            edit_portfolio_allocations(filename)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
