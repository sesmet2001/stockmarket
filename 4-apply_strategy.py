from pandas_datareader.data import DataReader
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import timeit
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
import vectorbt as vbt
from backtesting.lib import crossover
from strategies.Strat1 import Strat1
from strategies.Strat2 import Strat2
from strategies.TEMA_RSI import TEMA_RSI
from strategies.TEMA_RSI2 import TEMA_RSI2
from strategies.TEMA_RSI3 import TEMA_RSI3
from strategies.TEMA_RSI4 import TEMA_RSI4
from strategies.TEMA_RSI5 import TEMA_RSI5
import warnings

def cross_above_function(prev_val1,cur_val1,cur_val2):
    try:
        #print("prev_val1: " + str(prev_val1) + ", cur_val1: " + str(cur_val1) + ", cur_val2: " + str(cur_val2))
        if not (np.isnan(prev_val1) or np.isnan(cur_val1) or np.isnan(cur_val2)):
            if prev_val1 < cur_val2 and cur_val1 > cur_val2:
                return True
            else:
                return False       
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Exception occurred in cross on line {line_number}: {e}")

def cross_below_function(prev_val1,cur_val1,cur_val2):
    try:
        #print("prev_val1: " + str(prev_val1) + ", cur_val1: " + str(cur_val1) + ", cur_val2: " + str(cur_val2))
        if not (np.isnan(prev_val1) or np.isnan(cur_val1) or np.isnan(cur_val2)):
            if prev_val1 > cur_val2 and cur_val1 < cur_val2:
                return True
            else:
                return False     
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Exception occurred in cross on line {line_number}: {e}")

def main():
    warnings.filterwarnings("ignore")
    # PARAMETERS #
    chunksize = 100
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    my_plotrange = 100
    yf.pdr_override() 
    cross_above = np.vectorize(cross_above_function)
    cross_below = np.vectorize(cross_below_function)
    #print(sys.path)
    pd.set_option('display.max_rows', None)
    
    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
    cur_data = conn_data.cursor()
    conn_info = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
    cur_info = conn_info.cursor()

    my_start = datetime(2016, 1, 1)
    my_end = datetime.today().strftime('%Y-%m-%d')
    #my_end = datetime.strptime("2023-10-13", '%Y-%m-%d')
    print(my_start)
    print(my_end)

    # LOAD TICKER DATA #
    # test
    #my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE SP500 == 1 OR Dow == 1 OR Portfolio == 1 OR Oil == 1 OR Crypto == 1 OR PreciousMetals == 1 OR ExchangeRates == 1"""
    my_ticker_query = 'SELECT Ticker FROM _yahoo_fin_tickers WHERE (SP500 == 1 OR Dow == 1 OR Portfolio == 1 OR Crypto == 1 OR PreciousMetals == 1 OR Oil == 1 OR ExchangeRates == 1) AND (Ticker <> "BRK.B" OR Ticker <> "BF.B")'
       
    cur_info.execute(my_ticker_query)    
    my_tickers_list = cur_info.fetchall()
    my_tickers = [x[0] for x in my_tickers_list]
    #my_tickers = ["MSFT","NVDA"]
    my_strategies = ["Strat1", "Strat2"]

    for my_ticker in my_tickers:
        try:
            my_stock = Stock(conn_data,my_ticker,my_start,my_end)
            if type(my_stock.stockdata["AdjClose"].iloc[0]) == np.float64:
                print(my_stock.ticker)
                my_stock.stockdata["Strat1"] = Strat1(my_stock).define_position()
                #my_stock.stockdata["TEMA_RSI"] = TEMA_RSI(my_stock).define_position()
                #my_stock.stockdata["TEMA_RSI2"] = TEMA_RSI2(my_stock).define_position()    
                #my_stock.stockdata["TEMA_RSI3"] = TEMA_RSI3(my_stock).define_position()
                #my_stock.stockdata["TEMA_RSI4"] = TEMA_RSI4(my_stock).define_position()
                #my_stock.stockdata["TEMA_RSI5"] = TEMA_RSI5(my_stock).define_position()
                my_stock.stockdata.to_sql(my_ticker, conn_data, if_exists='replace', index = True) 

        except Exception as e:
            # Get the exception information including the line number
            exc_type, exc_obj, exc_tb = sys.exc_info()
                
            # Extract the line number
            line_number = exc_tb.tb_lineno
                
            # Print the exception message along with the line number
            print(f"Exception occurred in apply-strategy on line {line_number}: {e}")
            continue

    cur_data.close()
    conn_data.close()
    cur_info.close()
    conn_info.close()

if __name__ == "__main__":
    main()