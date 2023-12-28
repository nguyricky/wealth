import json
import os
from tabulate import tabulate

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
    save_allocations(filename, allocations)
    return allocations

def save_allocations(filename, allocations):
    with open(filename, 'w') as file:
        json.dump(allocations, file)

def edit_allocations(filename):
    allocations = load_or_create_allocations(filename)

    while True:
        print("\nCurrent Portfolio Allocations:")
        print(tabulate(allocations.items(), headers=["Stock", "Percentage"]))

        stock = input("Enter stock name to edit (or 'add' to add a new stock, 'remove' to remove a stock, 'done' to finish): ")

        if stock == 'done':
            break
        elif stock == 'add':
            new_stock = input("Enter new stock name: ")
            new_percentage = float(input(f"Enter allocation percentage for {new_stock}: "))
            if new_percentage < 0:
                print("Error: Allocation percentage cannot be negative.")
                continue
            if sum(allocations.values()) + new_percentage > 100:
                print("Error: This will exceed 100% total allocation. Try a smaller percentage.")
                continue
            allocations[new_stock] = new_percentage
        elif stock == 'remove':
            remove_stock = input("Enter stock name to remove: ")
            allocations.pop(remove_stock, None)
        else:
            if stock in allocations:
                current_total_excluding_stock = sum(perc for stk, perc in allocations.items() if stk != stock)
                new_percentage = float(input(f"Enter new allocation percentage for {stock}: "))
                if new_percentage < 0:
                    print("Error: Allocation percentage cannot be negative.")
                    continue
                if current_total_excluding_stock + new_percentage > 100:
                    print(f"Error: Total allocation exceeds 100%. You can allocate up to {100 - current_total_excluding_stock}% for {stock}.")
                    continue
                allocations[stock] = new_percentage
            else:
                print("Stock not found.")

    save_allocations(filename, allocations)

