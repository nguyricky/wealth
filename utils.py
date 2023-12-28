import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def scrape_stock(stock_symbol):
    url = f'https://www.google.com/search?q={stock_symbol}+stock+price'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_tag = soup.find('div', class_='BNeawe iBp4i AP7Wnd')

    if price_tag:
        price_text = price_tag.text.strip()
        parts = price_text.split()
        if len(parts) >= 3:
            price = parts[0]
            change, percent_change = parts[1], parts[2]
            return {
                'price': price,
                'change': change,
                'percent_change': percent_change.strip('()')
            }
        else:
            print(f"Unexpected format for stock price data: {price_text}")
            return None
    else:
        print(f"Could not find stock price for {stock_symbol}")
        return None

def fetch_multiple_stocks(stock_symbols):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(scrape_stock, stock_symbols)
    return list(results)

def fetch_stock_prices(allocations):
    stock_symbols = list(allocations.keys())
    scraped_data = fetch_multiple_stocks(stock_symbols)

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

def calculate_investment(allocations, total_investment):
    investment_per_stock = {}
    for stock, percentage in allocations.items():
        investment_per_stock[stock] = total_investment * (percentage / 100)
    return investment_per_stock
