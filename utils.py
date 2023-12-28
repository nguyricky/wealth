import requests

def fetch_stock_prices(allocations):
    prices = {}
    for stock in allocations.keys():
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey=0'
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