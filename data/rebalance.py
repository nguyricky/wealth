def rebalance_new(allocations, new_stock, new_percentage):
    total_percentage = sum(allocations.values())
    if total_percentage + new_percentage > 100:
        reduce_percentage = total_percentage + new_percentage - 100
        for stock in allocations:
            allocations[stock] *= (1 - (reduce_percentage / total_percentage))
            allocations[stock] = round(allocations[stock], 2)

        total_percentage = sum(allocations.values())
        if total_percentage != 100.0:
            last_stock = list(allocations.keys())[-1]
            allocations[last_stock] += round(100.0 - total_percentage, 2)

    allocations[new_stock] = new_percentage
    
def rebalance_remove(allocations):
    if not allocations or sum(allocations.values()) == 0:
        return allocations

    total_percentage = sum(allocations.values())
    remaining_percentage = 100 - total_percentage
    number_of_stocks = len(allocations)

    additional_per_stock = remaining_percentage / number_of_stocks
    for stock in allocations:
        allocations[stock] += additional_per_stock

    for stock in allocations:
        allocations[stock] = round(allocations[stock], 2)

    return allocations