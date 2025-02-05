from pandas_datareader.data import DataReader
import pandas as pd
from datetime import datetime, timedelta
import time
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
from backtesting.lib import crossover
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math
import numpy as np
from sqlalchemy import create_engine, Integer, String, Float, DateTime

def main():      
    #sys.stdout = open('log-21-concat-data.txt','w') 
    # PARAMETERS #
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    #conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite.db")
    engine = create_engine("sqlite:///" + DB_PATH + "/database/stockradar-lite.db", echo=True)
    #cur = conn.cursor()

    # LOAD ticker DATA #
    my_ticker_query = """SELECT * FROM _yahoo_fin_tickers WHERE screener == 1 OR dow == 1 OR sp500 == 1 OR nasdaq == 1 OR beursrally == 1 OR portfolio == 1 OR crypto == 1 OR preciousMetals == 1 OR exchangeRates == 1 OR oil == 1 OR crypto == 1 OR other == 1"""
    my_ticker_query = """SELECT * FROM _yahoo_fin_tickers WHERE sp500 == 1"""
    
    my_tickers = pd.read_sql(my_ticker_query, con=engine)
        
    my_final_df = pd.DataFrame()
    for index, row in my_tickers.iterrows():
        try:
            if (row['Ticker'] != "BRK.B" and row['Ticker'] != "BRK.A"):
                #print(row['Ticker'])
                my_data_query = "SELECT * from '" + row['Ticker'] + "'"
                my_data_df = pd.read_sql_query(my_data_query,con=engine)
                my_data_df['Ticker'] = row['Ticker']
                #my_data_df.set_index(["Date","Ticker"],inplace=True)
                my_final_df = pd.concat([my_final_df,my_data_df],ignore_index=True)
        #print(my_final_lst)
        #my_final_df = pd.concat(my_final_lst, ignore_index=False)
        except Exception as e:
            print(e)
            pass

    #my_final_df.index = my_final_df.index.astype(Integer)

    #my_final_df['Date'] = my_final_df['Date'].str.strip()
    #my_final_df['Date'] = pd.to_datetime(my_final_df['Date'])
    print(my_final_df.info())
    dtype_dict = {
        #"index": Integer(),
        "Date": DateTime(),
        "Open": Float(),
        "High": Float(),
        "Low": Float(),
        "Close": Float(),
        "Volume": Integer(),
        "Dividends": Float(),
        "Stock Splits": Float(),
        "BB_up": Float(),
        "BB_mid": Float(),
        "BB_low": Float(),
        "SMA10": Float(),
        "SMA50": Float(),
        "SMA150": Float(),
        "SMA200": Float(),
        "TEMA5": Float(),
        "TEMA10": Float(),
        "TEMA20": Float(),
        "TEMA50": Float(),
        "OBV": Float(),
        "RSI": Float(),
        "MACD": Float(),
        "MACDSignal": Float(),
        "MACDHist": Float(),
        "ClosePercentChange": Float(),
        "VolumePercentChange": Float(),
        "SMA50PercentChange": Float(),
        "prevTEMA5": Float(),
        "prevTEMA20": Float(),
        "prevSMA50": Float(),
        "prevRSI": Float(),
        "prevMACD": Float(),
        "prevMACDSignal": Float(),
        "MACD_slope": Float(),
        "MACD_sign_change": Float(),
        "30": Float(),
        "70": Float(),
        "Ticker": String(10),
        "Capital Gains": Float()
    }
    my_final_df.to_sql('all_stocks', con=engine, if_exists='replace', index=False,dtype=dtype_dict)
    engine.dispose()

if __name__ == "__main__":
    main()