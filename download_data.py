import yfinance as yf
import pandas as pd
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

tickers = ["AAPL", "MSFT", "SPY", "QQQ", "XLF", "GLD"]

# Download 5 years of data
raw_data = yf.download(tickers, period="5y")

# Extract Adjusted Close properly
adj_close = raw_data["Close"]

# Reset index
adj_close = adj_close.reset_index()

# Convert wide format to long format
data = adj_close.melt(id_vars=["Date"], var_name="Ticker", value_name="Adj Close")

# Save CSV
data.to_csv("data/historical_prices.csv", index=False)

print("Historical price data saved successfully.")