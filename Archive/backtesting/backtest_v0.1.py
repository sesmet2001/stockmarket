from stock import Stock
import yfinance as yf
import sqlite3
import os
import pandas as pd
import numpy as np
from indicators.volume import Volume
from indicators.bbands import BBands
from indicators.upseries import UpSeries
from indicators.downseries import DownSeries
from indicators.minervini import Minervini
from indicators.RSI import RSI
from indicators.BB import BB
import itertools
from datetime import date, datetime, timedelta
from collections import defaultdict

# def volume(my_stock):
#     signal = 0
#     my_stock.quotes['Volume_pctchange'] = my_stock.quotes['Volume'].pct_change()
#     if my_stock.quotes.iloc[-1,-1] > 25:
#         print(my_stock.quotes.iloc[-1,-1])
#         signal = 1
#     else:
#         signal = 0
#     return signal

# def close(my_stock):
#     signal = 0
#     my_stock.quotes['Close_pctchange'] = my_stock.quotes['Adj Close'].pct_change()
#     if my_stock.quotes.iloc[-1,-1] > 0.5:
#         print(my_stock.quotes.iloc[-1,-1])
#         signal = 1
#     else:
#         signal = 0
#     return signal

def main():
    try:
        conn = sqlite3.connect('/var/www/destef_be/stockradar.db')
        cur = conn.cursor()
    except Exception as e:
        print(e)
  
    start_date = None
    if start_date == None:
        start_date = datetime(2021, 9, 1)
    else:
        start_date = datetime.strptime(start_date[0], '%Y-%m-%d %H:%M:%S')
        start_date = start_date.date() + timedelta(days=2)
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    daterange = pd.date_range(start_date, end_date)
    
    for single_date in daterange:
        print (single_date.strftime("%Y-%m-%d"))
    
if __name__ == "__main__":
    main()
