from .tasks import fetch_stock_prices, check_alerts

def fetch_and_check_alerts():
    prices = fetch_stock_prices()
    if prices:
        check_alerts(prices)
