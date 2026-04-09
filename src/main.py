# Import necessary libraries
import yfinance as yf
import pandas as pd

# Define the ticker (SPY = S&P 500 ETF)
ticker = "SPY"

# Download historical data (last 5 years)
data = yf.download(ticker, start="2018-01-01", end="2023-01-01")

# Keep only the closing prices
data = data[['Close']]

# Rename column for clarity
data.columns = ['price']

# Display first rows
print(data.head())