from utils.scraper import scrape_stock
from concurrent.futures import ThreadPoolExecutor

def threads(stock_symbols):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(scrape_stock, stock_symbols)
    return list(results)