import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load S&P 500 stock symbols
sp500_symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

# Function to check if stock is above a moving average
def is_above_moving_average(stock_symbol, period):
    try:
        stock = yf.download(stock_symbol, period='6mo')
        if stock.empty:
            return False
        stock[f'{period}d_MA'] = stock['Close'].rolling(window=period).mean()
        return stock['Close'].iloc[-1] > stock[f'{period}d_MA'].iloc[-1]
    except Exception as e:
        print(f"Error with {stock_symbol}: {e}")
        return False

# Check for each moving average
above_20 = sum(is_above_moving_average(stock, 20) for stock in sp500_symbols)
above_50 = sum(is_above_moving_average(stock, 50) for stock in sp500_symbols)
above_100 = sum(is_above_moving_average(stock, 100) for stock in sp500_symbols)

# Plot the results
fig, ax = plt.subplots()
periods = ['20-Day MA', '50-Day MA', '100-Day MA']
counts = [above_20, above_50, above_100]

ax.bar(periods, counts)
ax.set_ylabel('Number of Stocks Above MA')
ax.set_title('S&P 500 Stocks Above Moving Averages')

for i, v in enumerate(counts):
    ax.text(i, v + 5, str(v), ha='center', va='bottom')

plt.show()
