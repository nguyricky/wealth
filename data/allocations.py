import json
import os
from questionary import form, text, Style as QuestionaryStyle, questionary
from rich.console import Console
from rich.table import Table
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
    console = Console()

    while True:
        table = Table(show_header=True, header_style="bold bright_white")
        table.add_column("Stock", style = "sky_blue1")
        table.add_column("Percentage", style = "green4")

        for stock, percentage in allocations.items():
            table.add_row(stock, f"{percentage}%")

        console.print("\nCurrent Portfolio Allocations:")
        console.print(table)
        print("\n")

        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Add stock",
                "Delete stock",
                "Edit stock percentage",
                "Done"
            ]).ask()

        if choice == "Done":
            break
        elif choice == "Add Stock":
            new_stock = questionary.text("Enter new stock name:").ask()
            new_percentage = questionary.text(f"Enter allocation percentage for {new_stock}:").ask()
            try:
                new_percentage = float(new_percentage)
                if new_percentage < 0:
                    print("Error: Allocation percentage cannot be negative.")
                    continue
                if sum(allocations.values()) + new_percentage > 100:
                    print("Error: This will exceed 100% total allocation. Try a smaller percentage.")
                    continue
                allocations[new_stock] = new_percentage
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == "Delete Stock":
            remove_stock = questionary.select("Select a stock to remove:", choices=list(allocations.keys())).ask()
            allocations.pop(remove_stock, None)
        elif choice == "Edit Stock Percentage":
            stock_to_edit = questionary.select("Select a stock to edit:", choices=list(allocations.keys())).ask()
            new_percentage = questionary.text(f"Enter new allocation percentage for {stock_to_edit}:").ask()
            try:
                new_percentage = float(new_percentage)
                current_total_excluding_stock = sum(perc for stk, perc in allocations.items() if stk != stock_to_edit)
                if new_percentage < 0:
                    print("Error: Allocation percentage cannot be negative.")
                    continue
                if current_total_excluding_stock + new_percentage > 100:
                    print(f"Error: Total allocation exceeds 100%. You can allocate up to {100 - current_total_excluding_stock}% for {stock_to_edit}.")
                    continue
                allocations[stock_to_edit] = new_percentage
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    save_allocations(filename, allocations)