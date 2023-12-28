import json
import os
from questionary import form, text, Style as QuestionaryStyle
from tabulate import tabulate
import colorama
from colorama import Fore, Style
colorama.init()

custom_style = QuestionaryStyle([
    ('question', 'noinherit'),
])

def load_or_create_allocations(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return create_new_allocations(filename)

def create_new_allocations(filename):
        
    print("\nPortfolio allocations file not found. Let's create a new one.")

    allocations = {}
    total_percentage = 0

    while total_percentage < 100:
        print(f"\nTotal allocated so far: {Style.BRIGHT}{Fore.GREEN}{total_percentage:.2f}%{Style.RESET_ALL}")

        response = form(
            stock = text("Enter stock name:", style = custom_style),
            percentage = text("Enter allocation percentage:", style = custom_style)
        ).ask()

        stock = response['stock']
        if stock.lower() == 'done':
            break

        try:
            percentage = float(response['percentage'])
            if percentage < 0 or percentage + total_percentage > 100:
                print("Error: Invalid allocation percentage. Please try again.")
                continue
            
            if stock in allocations:
                total_percentage -= allocations[stock]
                percentage += allocations[stock] 

            if total_percentage + percentage > 100:
                print("Error: Total allocation exceeds 100%. Please try again.")
                continue
        except ValueError:
            print("Error: Please enter a valid number.")
            continue

        allocations[stock] = percentage
        total_percentage += percentage

    if total_percentage != 100:
        print(f"Total allocation percentage is {total_percentage}%, which is not equal to 100%. Please start over.")
        return create_new_allocations(filename)

    with open(filename, 'w') as file:
        json.dump(allocations, file)
        
    print("\n")

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

