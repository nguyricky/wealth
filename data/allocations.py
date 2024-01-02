import json
import os
from questionary import form, text, Style as QuestionaryStyle, questionary
from rich.console import Console
from rich.table import Table
import colorama
from colorama import Fore, Style
from data.rebalance import rebalance_new, rebalance_remove

colorama.init()
previous_allocations = None

custom_style = QuestionaryStyle([
    ('question', 'noinherit'),
])

def get_previous_allocations():
    global previous_allocations
    return previous_allocations

def set_previous_allocations(allocations):
    global previous_allocations
    previous_allocations = allocations

def display_portfolio(allocations):
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Stock", justify="left")
    table.add_column("Percentage", justify="right")

    for stock, percentage in allocations.items():
        table.add_row(stock, f"{percentage}%")

    console.print("\nPortfolio Allocations:")
    console.print(table)

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
    set_previous_allocations(allocations.copy())
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
                "Add Stock",
                "Delete Stock",
                "Edit Stock Percentage",
                "Done"
            ]).ask()

        if choice == "Done":
            break
        elif choice == "Add Stock":
            new_stock = questionary.text("Enter new stock name:").ask()
            new_percentage = questionary.text(f"Enter desired portfolio percentage for {new_stock}:").ask()

            try:
                new_percentage = float(new_percentage)
                if new_percentage <= 0 or new_percentage > 100:
                    console.print("Error: Allocation percentage must be between 0 and 100.")
                    continue

                rebalance_new(allocations, new_stock, new_percentage)
            except ValueError:
                console.print("Invalid input. Please enter a valid number.")
        elif choice == "Delete Stock":
            if allocations:
                remove_stock = questionary.select(
                    "Select a stock to remove:", 
                    choices=list(allocations.keys())
                ).ask()

                if remove_stock and remove_stock in allocations:
                    allocations.pop(remove_stock)
                    console.print(f"\n{remove_stock} removed from portfolio.")

                    rebalance_choice = questionary.select(
                        "Would you like to rebalance your portfolio now?",
                        choices=["Rebalance Portfolio", "Done"]
                    ).ask()

                    if rebalance_choice == "Rebalance Portfolio":
                        allocations = rebalance_remove(allocations)
                        console.print("\nPortfolio rebalanced:")
                        display_portfolio(allocations)
                    elif rebalance_choice == "Done":
                        console.print("No changes made to the remaining allocations.")
                else:
                    console.print("Stock not found in portfolio.")
            else:
                console.print("No stocks available to delete.")
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