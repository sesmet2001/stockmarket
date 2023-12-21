from pandas_datareader.data import DataReader
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import timeit
import sqlite3
import numpy as np
import sqlite3
import os
import talib.abstract as ta
from base.stock import Stock

def main():

    # PARAMETERS #
    chunksize = 100
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    yf.pdr_override() 
    
    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
    cur_data = conn_data.cursor()
    conn_info = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
    cur_info = conn_info.cursor()

    # DEFINE START END #########
    sqlexists = """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CRM'"""
    cur_data.execute(sqlexists)
    if cur_data.fetchone()[0]==1:
            print('Table exists.')
            sqldates = """SELECT Date FROM CRM ORDER BY Date DESC LIMIT 1"""
            start = cur_data.execute(sqldates).fetchone()
            start = datetime.strptime(start[0], '%Y-%m-%dT%H:%M:%S')
            start = start.date() + timedelta(days=2)
    else:
            start = datetime(2020, 1, 1)

    #start = datetime(2021, 1, 1)
    my_end = datetime.today().strftime('%Y-%m-%d')
    print(start)
    print(my_end)

    # LOAD TICKER DATA #
    # my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR PreciousMetals == 1 OR Crypto == 1 OR Portfolio == 1"""
    my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Portfolio == 1 OR Dow == 1"""
    cur_info.execute(my_ticker_query)    
    my_tickers_list = cur_info.fetchall()
    my_tickers = [x[0] for x in my_tickers_list]
    my_tickers = ["CRM"]

    for my_ticker in my_tickers:
        try:
            my_stock = Stock()
            sql_stock = pd.read_sql_query("SELECT * from '" + my_ticker + "' WHERE Date <= '" + str(my_end) + "'",conn_data)
            my_stock_df = pd.DataFrame(sql_stock)
            if type(my_stock_df["AdjClose"].iloc[0:1][0]) == np.float64:
                my_stock_df.dropna(subset=['Close'], inplace=True)
                my_stock_df['BB_up'], my_stock_df['BB_mid'], my_stock_df['BB_low'] = ta.BBANDS(my_stock_df['Close'], timeperiod=20)
                my_stock_df["SMA10"] = ta.SMA(my_stock_df['Close'],10)
                my_stock_df["SMA50"] = ta.SMA(my_stock_df['Close'],50)
                my_stock_df["SMA150"] = ta.SMA(my_stock_df['Close'],150)
                my_stock_df["SMA200"] = ta.SMA(my_stock_df['Close'],200)
                my_stock_df["TEMA5"] = ta.TEMA(my_stock_df['Close'],5)
                my_stock_df["TEMA10"] = ta.TEMA(my_stock_df['Close'],10)
                my_stock_df["TEMA20"] = ta.TEMA(my_stock_df['Close'],20)
                my_stock_df["TEMA50"] = ta.TEMA(my_stock_df['Close'],50)
                my_stock_df["RSI"] = ta.RSI(my_stock_df['Close'],timeperiod=6)
                my_stock_df['MACD'], my_stock_df['MACDSignal'], my_stock_df['MACDHist'] = ta.MACD(my_stock_df['Close'], fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
                my_stock_df['ClosePercentChange'] = my_stock_df['AdjClose'].pct_change()
                my_stock_df['VolumePercentChange'] = my_stock_df['Volume'].pct_change()
                my_stock_df['SMA50PercentChange'] = my_stock_df['SMA50'].pct_change()
                my_stock_df['ClosePercentChange'] = my_stock_df['AdjClose'].pct_change()
                my_stock_df.to_sql(my_ticker, conn_data, if_exists='replace', index = False)
        except:
            print(my_ticker + ": An exception occurred")
            continue

    cur_data.close()
    conn_data.close()
    cur_info.close()
    conn_info.close()

if __name__ == "__main__":
    main()