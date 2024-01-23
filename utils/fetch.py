from utils.scraper import scrape_stock
from concurrent.futures import ThreadPoolExecutor

def threads(stock_symbols):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(scrape_stock, stock_symbols)
    return list(results)

def fetch_stock_prices(allocations):
    stock_symbols = list(allocations.keys())
    scraped_data = threads(stock_symbols)

    stock_data = {}
    for stock, data in zip(stock_symbols, scraped_data):
        if data:
            try:
                stock_data[stock] = {
                    'price': float(data['price'].replace(',', '')),
                    'change': data['change'],
                    'percent_change': data['percent_change']
                }
            except ValueError:
                print(f"Error parsing data for {stock}: {data}")
        else:
            stock_data[stock] = None
    return stock_data
