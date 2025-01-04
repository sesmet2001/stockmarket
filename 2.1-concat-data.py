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

def main():      
    # PARAMETERS #
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    my_data_conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
    cur_data = my_data_conn.cursor()
    my_tickers_conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite-tickers.db")
    cur_tickers = my_tickers_conn.cursor()

    # LOAD ticker DATA #
    #my_ticker_query = """SELECT * FROM _yahoo_fin_tickers WHERE screener == 1 OR dow == 1 OR sp500 == 1 OR nasdaq == 1 OR beursrally == 1 OR portfolio == 1 OR crypto == 1 OR preciousMetals == 1 OR exchangeRates == 1 OR oil == 1 OR crypto == 1 OR other == 1"""
    my_ticker_query = """SELECT * FROM _yahoo_fin_tickers WHERE beursrally == 1"""
    
    my_tickers = pd.read_sql(my_ticker_query, my_tickers_conn)
    
    try:
        my_final_df = pd.DataFrame()
        for index, row in my_tickers.iterrows():
            if row['Ticker'] != "BRK.B":
                print(row['Ticker'])
                my_data_query = "SELECT * from '" + row['Ticker'] + "'"
                my_data_df = pd.read_sql_query(my_data_query,my_data_conn)
                my_data_df['Ticker'] = row['Ticker']
                my_data_df.set_index(["Date","Ticker"],inplace=True)
                my_final_df = pd.concat([my_final_df,my_data_df],ignore_index=True)
        #print(my_final_lst)
        #my_final_df = pd.concat(my_final_lst, ignore_index=False)

        #my_final_df.to_sql('all_stocks', my_data_conn, if_exists='replace', index=True)
        cur_data.close()
        my_data_conn.close()
        cur_tickers.close()
        my_tickers_conn.close()
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()