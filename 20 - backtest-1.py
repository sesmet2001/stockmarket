from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd
from backtesting.test import GOOG
from backtesting import Backtest
from strategies.SmaCross import SmaCross
import sqlite3
import os
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from base.stock import Stock
import sys

def main():
    my_plotrange = 100
    my_strategy = "X_TEMA5_TEMA20"
    my_format = '%Y-%m-%d %H:%M:%S'
    yf.pdr_override() 
    
    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
    cur_data = conn_data.cursor()
    conn_info = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
    cur_info = conn_info.cursor()

    my_start = datetime(2020, 1, 1)
    my_end = datetime.today().strftime('%Y-%m-%d')
    #my_end = datetime.strptime("2023-10-13", '%Y-%m-%d')
    print(my_start)
    print(my_end)


    # LOAD TICKER DATA #
    my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR Portfolio == 1 AND Ticker != 'ARM' OR Crypto == 1 OR PreciousMetals == 1 LIMIT 1"""
    cur_info.execute(my_ticker_query)    
    my_tickers_list = cur_info.fetchall()
    my_tickers = [x[0] for x in my_tickers_list]
    my_tickers = ["MSFT","NVDA"]

    for my_ticker in my_tickers:
        try:
            my_stock = Stock(conn_data,my_ticker,my_end)
            if type(my_stock.stockdata["AdjClose"].iloc[0:1][0]) == np.float64:
                print(my_stock.ticker)
                my_stock.stockdata.set_index(pd.DatetimeIndex(my_stock.stockdata['Date']), inplace=True)
                my_stockdf = my_stock.stockdata[["Open", "High", "Low", "Close", "Volume"]]
                bt = Backtest(my_stockdf, SmaCross, cash=10_000, commission=.002)
                stats = bt.run()
                print(stats['_trades'])
                bt.plot()
        except Exception as e:
                    # Get the exception information including the line number
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    
                    # Extract the line number
                    line_number = exc_tb.tb_lineno
                    
                    # Print the exception message along with the line number
                    print(f"Exception occurred in backtest-1 on line {line_number}: {e}")
                    continue

    cur_data.close()
    conn_data.close()
    cur_info.close()
    conn_info.close()




if __name__ == "__main__":
    main()