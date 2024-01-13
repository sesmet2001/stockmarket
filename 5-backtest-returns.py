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
from strategies.TEMA_RSI import TEMA_RSI

def main():
    # PARAMETERS #
    chunksize = 100
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    my_plotrange = 100
    my_strategies = ["TEMA_RSI","TEMA_RSI2","TEMA_RSI3"]
    my_starting_balance = 10000
    yf.pdr_override() 
    #print(sys.path)
    
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
    # test
    # my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR PreciousMetals == 1 OR Crypto == 1 OR Portfolio == 1"""
    my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR Portfolio == 1 OR Oil == 1 OR Crypto == 1 OR PreciousMetals == 1"""
    #my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Portfolio == 1"""
    cur_info.execute(my_ticker_query)    
    my_tickers_list = cur_info.fetchall()
    my_tickers = [x[0] for x in my_tickers_list]
    #my_tickers = ["MSFT","NVDA"]


    total_stocks = 0
    for my_ticker in my_tickers:
        try:
            total_stocks = total_stocks + 1
            my_stock = Stock(conn_data,my_ticker,my_start,my_end)
            my_stock.plotdata = my_stock.stockdata.tail(my_plotrange).copy()
            my_stock.plotdata['DailyReturn'] = my_stock.plotdata['Close'] / my_stock.plotdata['Open'] 
            my_stock.plotdata['CumulativeReturn'] = my_stock.plotdata['DailyReturn'].cumprod()
            my_stock.plotdata['CumulativeReturnPeak'] = my_stock.plotdata['CumulativeReturn'].cummax()
            my_stock.plotdata['Drawdown'] = my_stock.plotdata['CumulativeReturn'] - my_stock.plotdata['CumulativeReturnPeak']
            if type(my_stock.stockdata["AdjClose"].iloc[0:1][0]) == np.float64:
                for my_strategy in my_strategies:
                    my_stock.plotdata[my_strategy + '_return'] = np.where(my_stock.plotdata[my_strategy].shift(1)== True, my_stock.plotdata["DailyReturn"], 1.0) 
                    my_stock.plotdata[my_strategy + '_total_return'] = my_starting_balance * my_stock.plotdata[my_strategy + '_return'].cumprod()
                    my_stock.plotdata.to_sql(my_ticker, conn_data, if_exists='replace', index = False)
                    print(my_stock.ticker + ": " + str(round(my_stock.plotdata[my_strategy + '_total_return'].iloc[-1])))
            

        except Exception as e:
            # Get the exception information including the line number
            exc_type, exc_obj, exc_tb = sys.exc_info()
            
            # Extract the line number
            line_number = exc_tb.tb_lineno
            
            # Print the exception message along with the line number
            print(f"Exception occurred in backtest-returns on line {line_number}: {e}")
            continue

    for my_strategy in my_strategies:
        total_stocks = 0
        total_return = 0
        for my_ticker in my_tickers:
            total_stocks = total_stocks + 1
            my_stock = Stock(conn_data,my_ticker,my_start,my_end)
            my_stock.plotdata = my_stock.stockdata.tail(my_plotrange).copy()
            total_return = total_return + my_stock.plotdata[my_strategy + '_total_return'].iloc[-1]
        my_return = round(total_return - (10000*total_stocks))
        my_investment = round(10000*total_stocks)
        my_pct_return = (total_return - (10000*total_stocks))/total_return*100
        print("Total Return " + my_strategy + ": " + str(my_return) + "$ on investment of " + str(my_investment) + "$ (" + str(round(my_pct_return,2)) + "%)")

    cur_data.close()
    conn_data.close()
    cur_info.close()
    conn_info.close()

if __name__ == "__main__":
    main()