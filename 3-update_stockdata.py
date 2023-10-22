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

def find_TEMA5_SMA50_crossover(TEMA5, prevTEMA5,SMA50):
    if TEMA5 > SMA50 and prevTEMA5 < SMA50:
        return "bullish crossover"
    elif TEMA5 < SMA50 and prevTEMA5 > SMA50:
        return "bearish crossover"
    return None

def find_TEMA5_TEMA20_RSI_crossover(TEMA5,prevTEMA5,prevTEMA20,TEMA20,RSI):
    if TEMA5 > TEMA20 and prevTEMA5 < prevTEMA20 and RSI < 35:
        return "bullish crossover"
    elif TEMA5 < TEMA20 and prevTEMA5 > prevTEMA20 and RSI > 65:
        return "bearish crossover"
    else:
        return None

def find_TEMA5_TEMA20_crossover(TEMA5,prevTEMA5,prevTEMA20,TEMA20):
    if TEMA5 > TEMA20 and prevTEMA5 < prevTEMA20:
        return "bullish crossover"
    elif TEMA5 < TEMA20 and prevTEMA5 > prevTEMA20:
        return "bearish crossover"
    else:
        return None

def main():

    # PARAMETERS #
    chunksize = 100
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    my_plotrange = 100
    yf.pdr_override() 

    print(sys.path)
    
    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
    cur_data = conn_data.cursor()
    conn_info = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
    cur_info = conn_info.cursor()

    # DEFINE START END #########
    #sqlexists = """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CRM'"""
    #cur_data.execute(sqlexists)
    #if cur_data.fetchone()[0]==1:
    #        print('Table exists.')
    #        sqldates = """SELECT Date FROM CRM ORDER BY Date DESC LIMIT 1"""
    #        my_start = cur_data.execute(sqldates).fetchone()
    #        if socket.gethostname() == "aldix":
    #            my_start = datetime.strptime(my_start[0], '%Y-%m-%d %H:%M:%S')
    #        else:
    #            my_start = datetime.strptime(my_start[0], '%Y-%m-%dT%H:%M:%S')
    #        #my_start = datetime.strptime(my_start[0])
    #        my_start = my_start.date() + timedelta(days=1)
    #else:
    #        my_start = datetime(2020, 1, 1)

    my_start = datetime(2020, 1, 1)
    my_end = datetime.today().strftime('%Y-%m-%d')
    #my_end = datetime.strptime("2023-10-13", '%Y-%m-%d')
    print(my_start)
    print(my_end)


    # LOAD TICKER DATA #
    # my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR PreciousMetals == 1 OR Crypto == 1 OR Portfolio == 1"""
    my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR Portfolio == 1"""
    cur_info.execute(my_ticker_query)    
    my_tickers_list = cur_info.fetchall()
    my_tickers = [x[0] for x in my_tickers_list]
    #my_tickers = ["AAPL","CRM"]

    # DOWNLOAD DATA IN CHUNKS #
    chunks = [my_tickers[i:i + chunksize] for i in range(0, len(my_tickers), chunksize)]
    try:
        for chunk in chunks:
            print(str(chunk) + "\n")
            data = yf.download(" ".join(chunk),start=my_start,end=my_end,actions=False)
            for my_ticker in chunk:
                my_ticker_df = data.loc[:,[("Adj Close",my_ticker),("Close",my_ticker),("High",my_ticker),("Low",my_ticker),("Open",my_ticker),("Volume",my_ticker)]]
                my_ticker_df.columns = ["AdjClose","Close","High","Low","Open","Volume"]
                #my_ticker_df["Ticker"] = my_ticker
                if not pd.isnull(my_ticker_df['AdjClose']).all():
                    my_ticker_df.to_sql(my_ticker, conn_data, if_exists='replace')
                else:
                    print(my_ticker + " has no data.")
    except Exception as e:
        print(e)
        pass
    
    for my_ticker in my_tickers:
        try:
            my_stock = Stock(conn_data,my_ticker,my_end)
            if type(my_stock.stockdata["AdjClose"].iloc[0:1][0]) == np.float64:
                my_stock.dropna()
                my_stock.stockdata['BB_up'], my_stock.stockdata['BB_mid'], my_stock.stockdata['BB_low'] = ta.BBANDS(my_stock.stockdata['Close'], timeperiod=20)
                my_stock.stockdata["SMA10"] = ta.SMA(my_stock.stockdata['Close'],10)
                my_stock.stockdata["SMA50"] = ta.SMA(my_stock.stockdata['Close'],50)
                my_stock.stockdata["SMA150"] = ta.SMA(my_stock.stockdata['Close'],150)
                my_stock.stockdata["SMA200"] = ta.SMA(my_stock.stockdata['Close'],200)
                my_stock.stockdata["TEMA5"] = ta.TEMA(my_stock.stockdata['Close'],5)
                my_stock.stockdata["TEMA10"] = ta.TEMA(my_stock.stockdata['Close'],10)
                my_stock.stockdata["TEMA20"] = ta.TEMA(my_stock.stockdata['Close'],20)
                my_stock.stockdata["TEMA50"] = ta.TEMA(my_stock.stockdata['Close'],50)
                my_stock.stockdata["RSI"] = ta.RSI(my_stock.stockdata['Close'],timeperiod=6)
                my_stock.stockdata['MACD'], my_stock.stockdata['MACDSignal'], my_stock.stockdata['MACDHist'] = ta.MACD(my_stock.stockdata['Close'], fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
                my_stock.stockdata['ClosePercentChange'] = my_stock.stockdata['AdjClose'].pct_change()
                my_stock.stockdata['VolumePercentChange'] = my_stock.stockdata['Volume'].pct_change()
                my_stock.stockdata['SMA50PercentChange'] = my_stock.stockdata['SMA50'].pct_change()
                my_stock.stockdata['ClosePercentChange'] = my_stock.stockdata['AdjClose'].pct_change()
                my_stock.stockdata['prevTEMA5'] = my_stock.stockdata['TEMA5'].shift(1)
                my_stock.stockdata['prevTEMA20'] = my_stock.stockdata['TEMA20'].shift(1)
                my_stock.stockdata['prevRSI'] = my_stock.stockdata['RSI'].shift(1)
                my_stock.stockdata.dropna(inplace=True)
                
                my_stock.stockdata['TEMA5_TEMA20_crossover'] = np.vectorize(find_TEMA5_TEMA20_RSI_crossover)(my_stock.stockdata["TEMA5"],my_stock.stockdata["prevTEMA5"],my_stock.stockdata["prevTEMA20"],my_stock.stockdata["TEMA20"],my_stock.stockdata["prevRSI"],my_stock.stockdata["RSI"])               my_stock.plotbasegraph(DB_PATH + "/graphs" + "/",my_plotrange)
                my_stock.stockdata.to_sql(my_ticker, conn_data, if_exists='replace', index = False)
        except Exception as e:
            print(my_ticker + ": An exception " + str(e) + " occurred")
            continue

    cur_data.close()
    conn_data.close()
    cur_info.close()
    conn_info.close()

if __name__ == "__main__":
    main()