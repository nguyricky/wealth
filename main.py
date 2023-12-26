import json
import os
import requests

def load_or_create_allocations(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return create_new_allocations(filename)

def create_new_allocations(filename):
    allocations = {}
    total_percentage = 0
    print("Portfolio allocations file not found. Let's create a new one.")
    print("Enter your portfolio allocations (enter 'done' to finish):")
    while total_percentage < 100:
        stock = input("Enter stock name: ")
        if stock.lower() == 'done':
            break
        percentage = float(input(f"Enter allocation percentage for {stock} (Total so far: {total_percentage}%): "))
        if total_percentage + percentage > 100:
            print(f"Error: Total allocation exceeds 100%. You can allocate up to {100 - total_percentage}% more.")
            continue
        allocations[stock] = percentage
        total_percentage += percentage
    with open(filename, 'w') as file:
        json.dump(allocations, file)
    return allocations

def edit_portfolio_allocations(filename, allocations):
    total_percentage = sum(allocations.values())
    print("Editing portfolio allocations. Enter 'done' to finish.")
    while total_percentage < 100:
        stock = input("Enter stock name (or 'done' to finish): ")
        if stock.lower() == 'done':
            break
        percentage = float(input(f"Enter allocation percentage for {stock} (Total so far: {total_percentage}%): "))
        if total_percentage - allocations.get(stock, 0) + percentage > 100:
            print(f"Error: Total allocation exceeds 100%. You can allocate up to {100 - (total_percentage - allocations.get(stock, 0))}% more.")
            continue
        allocations[stock] = percentage
        total_percentage = sum(allocations.values())
    with open(filename, 'w') as file:
        json.dump(allocations, file)

def fetch_stock_prices(allocations):
    prices = {}
    for stock in allocations.keys():
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey=YOUR_API_KEY'
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
    allocations = load_or_create_allocations(filename)

    while True:
        print("\n--- Menu ---\n")
        print("1. Enter investment amount")
        print("2. Fetch current stock prices")
        print("3. Edit portfolio allocations")
        print("4. Exit")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            total_investment = float(input("Enter the total investment amount: "))
            investment_per_stock = calculate_investment(allocations, total_investment)
            
            print("\nInvestment Allocation:")
            for stock, amount in investment_per_stock.items():
                print(f"{stock}: ${amount:.2f}")
        elif choice == '2':
            prices = fetch_stock_prices(allocations)
            print("\nCurrent Stock Prices:", prices)
        elif choice == '3':
            edit_portfolio_allocations(filename, allocations)
            allocations = load_or_create_allocations(filename)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
