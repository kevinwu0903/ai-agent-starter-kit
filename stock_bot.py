import argparse
import csv
import os
import time
from datetime import datetime

import yfinance as yf


def fetch_prices(tickers):
    prices = {}
    for symbol in tickers:
        try:
            info = yf.Ticker(symbol).fast_info
            price = info.get("lastPrice")
            if price is not None:
                prices[symbol] = price
        except Exception as exc:
            print(f"Error fetching {symbol}: {exc}")
    return prices


def save_to_csv(prices, filename):
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "ticker", "price"])
        timestamp = datetime.utcnow().isoformat()
        for symbol, price in prices.items():
            writer.writerow([timestamp, symbol, price])


def run(interval, tickers, output):
    while True:
        data = fetch_prices(tickers)
        if data:
            save_to_csv(data, output)
            print(f"[{datetime.utcnow().isoformat()}] Saved: {data}")
        else:
            print(f"[{datetime.utcnow().isoformat()}] No data fetched")
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Automatically collect stock prices using Yahoo Finance")
    parser.add_argument("--tickers", nargs="+", default=["AAPL", "MSFT"], help="Ticker symbols to fetch")
    parser.add_argument("--interval", type=int, default=60, help="Time between fetches in seconds")
    parser.add_argument("--output", default="stock_data.csv", help="CSV file to store results")
    args = parser.parse_args()

    run(args.interval, args.tickers, args.output)


if __name__ == "__main__":
    main()
