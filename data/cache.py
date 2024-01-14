import json

previous_allocations = None

def save_allocations(filename, allocations):
    with open(filename, 'w') as file:
        json.dump(allocations, file)

def get_previous_allocations():
    global previous_allocations
    return previous_allocations

def set_previous_allocations(allocations):
    global previous_allocations
    previous_allocations = allocations

def revert_allocations(filename):
    global previous_allocations
    if previous_allocations is not None:
        save_allocations(filename, previous_allocations)
        print("Reverted to the previous state.")
    else:
        print("No previous state to revert to.")

