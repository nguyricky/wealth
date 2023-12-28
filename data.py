import json
import os

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