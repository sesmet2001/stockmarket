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
    chunksize = 100
    max_retries = 3
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    my_plotrange = 100
    my_start = datetime(2022, 1, 1)
    my_strategy = "X_TEMA5_TEMA20"
    start_time = datetime.now()
    #yf.pdr_override() 
    remaining_tickers = []
    #print(sys.path)
    pd.set_option('display.max_rows', 10)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    #np.set_printoptions(threshold=np.inf)
    if len(sys.argv) > 1:
        my_end = datetime.strptime(sys.argv[1], "%Y-%m-%d")     
    else:
        my_end = datetime.today().strftime('%Y-%m-%d')

    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
    cur_data = conn_data.cursor()
    conn_tickers = sqlite3.connect(DB_PATH + "/database/stockradar-lite-tickers.db")
    cur_tickers = conn_tickers.cursor()

    # LOAD ticker DATA #
    my_ticker_query = """SELECT ticker FROM _yahoo_fin_tickers WHERE screener == 1 OR dow == 1 OR sp500 == 1 OR nasdaq == 1 OR beursrally == 1 OR portfolio == 1 OR crypto == 1 OR preciousMetals == 1 OR exchangeRates == 1 OR oil == 1 OR crypto == 1 OR other == 1"""
    my_tickers = pd.read_sql(my_ticker_query, conn_tickers)


    #my_tickers['ticker'] = my_tickers['ticker'].replace('BRK.A', 'BRK-A')
    #my_tickers['ticker'] = my_tickers['ticker'].replace('BRK.B', 'BRK-B')
    #my_tickers['ticker'] = my_tickers['ticker'].replace('BF.B', 'BF-B')
    #my_tickers['ticker'] = my_tickers['ticker'].replace('PBR.A', 'PBR-A')
    #my_tickers['ticker'] = my_tickers['ticker'].replace('LEN.B', 'LEN-B')
    #my_tickers['ticker'] = my_tickers['ticker'].replace('HEI.A', 'HEI-A')
    #my_tickers['ticker'] = my_tickers['ticker'].replace('VUSA.AS', 'VUSA-AS')
    #my_tickers.set_index('ticker', inplace=True)

    print("Stock data from " + str(my_start) + " until " + str(my_end))
    for index, row in my_tickers.iterrows():
        if index % 500 == 0:
            time.sleep(60)
        my_log = str(index) + ": " + row['ticker'] + " (Start: " + str(start_time) + " - Current: " + str(datetime.now()) + ")"
        print(my_log)
        try: 
            my_ticker = yf.Ticker(row['ticker'])
            my_ticker_df = my_ticker.history(start=my_start,end=my_end)
            #print(my_ticker_df)
            if not pd.isnull(my_ticker_df['Close']).all():
                my_ticker_df.to_sql(row['ticker'], conn_data, if_exists='replace')
            else:
                print(row['ticker'] + " has no data.")
                remaining_tickers.append[my_log]
        except Exception as e:
            # Print error message and traceback details
            print("An error occurred:")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {e}")
            traceback_details = traceback.format_exc()
            print(f"Traceback Details:\n{traceback_details}")
    print(remaining_tickers)
    cur_data.close()
    conn_data.close()
    cur_tickers.close()
    conn_tickers.close()

if __name__ == "__main__":
    main()