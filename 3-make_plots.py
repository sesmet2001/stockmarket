# v0.1

from pandas_datareader.data import DataReader
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import time
import sqlite3
import numpy as np
import sqlite3
import os
import sys
import talib.abstract as ta
from base.stock import Stock
import socket
from patterns.cross import Cross
import traceback
from backtesting.lib import crossover
from strategies.TEMA_RSI import TEMA_RSI

def main():
    sys.stdout = open('./log-3-make_plots.txt','w') 
    # PARAMETERS #
    chunksize = 100
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    my_plotrange = 200
    my_strategies = ["Strat1"]
    my_colors = ["red","green","blue"]
    #yf.pdr_override() 
    print(sys.path)
    
    # DB CONNECTIONS #
    if os.name == 'nt':
        DB_PATH='C:/wamp64/www/html/'
    else:
        DB_PATH='/var/www/html/'
    conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite.db")
    cur = conn.cursor()

    my_start = datetime(2024, 1, 1)
    my_end = datetime.today().strftime('%Y-%m-%d')
    #my_end = datetime.strptime("2023-10-13", '%Y-%m-%d')
    print(my_start)
    print(my_end)

    # LOAD TICKER DATA #
    # test
    #my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE SP500 == 1 OR Dow == 1 OR Portfolio == 1 OR Oil == 1 OR Crypto == 1 OR PreciousMetals == 1 OR ExchangeRates == 1"""
    #my_ticker_query = 'SELECT Ticker, Company FROM _yahoo_fin_tickers WHERE (Screener == 1 OR Beursrally == 1 OR SP500 == 1 OR Dow == 1 OR Other == 1 OR Crypto == 1 OR PreciousMetals == 1 OR Oil == 1 OR ExchangeRates == 1)'
    my_ticker_query = 'SELECT Ticker,Company FROM _yahoo_fin_tickers WHERE (Screener == 1 OR Beursrally == 1 OR Portfolio == 1 OR SP500 == 1 OR Dow == 1 OR Nasdaq == 1 OR Other == 1 OR Crypto == 1 OR PreciousMetals == 1 OR Oil == 1 OR ExchangeRates == 1)'    
    #my_ticker_query = 'SELECT Ticker, Company FROM _yahoo_fin_tickers WHERE Ticker == "ADBE"'
    #my_ticker_query = 'SELECT Ticker, Company FROM _yahoo_fin_tickers WHERE Ticker=="AAPL"'
    #my_ticker_query = 'SELECT Ticker, Company FROM _yahoo_fin_tickers WHERE (Beursrally == 1 OR Portfolio == 1 OR Other == 1 OR Crypto == 1 OR PreciousMetals == 1 OR Oil == 1 OR ExchangeRates == 1)'    

    cur.execute(my_ticker_query)    
    my_tickers_list = cur.fetchall()
    my_tickers = [x for x in my_tickers_list]
    print(len(my_tickers_list))
    #my_tickers = [x[0] for x in my_tickers_list]
    #print(my_tickers)
    #my_tickers = ["BABA","CRWD"]
    #print(my_tickers)

    for my_ticker,my_company in my_tickers:
        try:
            print(my_ticker)
            my_stock = Stock(conn,my_ticker,my_company,my_start,my_end)
            if type(my_stock.stockdata["Close"].iloc[0]) == np.float64:
                start_time = time.time()
                my_stock.plotbasegraph(DB_PATH + "/graphs/",my_plotrange,my_strategies,my_colors)
                end_time = time.time()
                duration = end_time - start_time
                print(f"Duration: {duration:.2f} seconds")
               

        except Exception as e:
            # Get the exception information including the line number
            exc_type, exc_obj, exc_tb = sys.exc_info()
            
            # Extract the line number
            line_number = exc_tb.tb_lineno
            
            # Print the exception message along with the line number
            print(f"Exception occurred in update-stockdata on line {line_number}: {e}")
            continue

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()