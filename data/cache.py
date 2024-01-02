from data.allocations import get_previous_allocations, save_allocations

def revert_allocations(filename):
    previous_allocations = get_previous_allocations()
    if previous_allocations:
        save_allocations(filename, previous_allocations)
        print("Reverted to the previous state.")
    else:
        print("No previous state to revert to.")
