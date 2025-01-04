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
    #my_ticker_query = """SELECT * FROM _yahoo_fin_tickers WHERE screener == 1 OR dow == 1 OR sp500 == 1 OR nasdaq == 1 OR beursrally == 1 OR portfolio == 1 OR crypto == 1 OR preciousMetals == 1 OR exchangeRates == 1 OR oil == 1 OR crypto == 1 OR other == 1"""
    my_ticker_query = """SELECT * FROM _yahoo_fin_tickers WHERE beursrally == 1"""
    
    my_tickers = pd.read_sql(my_ticker_query, conn_tickers)


    #my_tickers['Ticker'] = my_tickers['Ticker'].replace('BRK.A', 'BRK-A')
    my_tickers['Ticker'] = my_tickers['Ticker'].replace('BRK.B', 'BRK-B')
    #my_tickers['Ticker'] = my_tickers['Ticker'].replace('BF.B', 'BF-B')
    #my_tickers['Ticker'] = my_tickers['Ticker'].replace('PBR.A', 'PBR-A')
    #my_tickers['Ticker'] = my_tickers['Ticker'].replace('LEN.B', 'LEN-B')
    #my_tickers['Ticker'] = my_tickers['Ticker'].replace('HEI.A', 'HEI-A')
    #my_tickers['Ticker'] = my_tickers['Ticker'].replace('VUSA.AS', 'VUSA-AS')
    #my_tickers.set_index('ticker', inplace=True)

    print("Stock data from " + str(my_start) + " until " + str(my_end))
    for index, row in my_tickers.iterrows():
        if index % 500 == 0:
            time.sleep(60)
        my_log = str(index) + ": " + row['Ticker'] + " (Start: " + str(start_time) + " - Current: " + str(datetime.now()) + ")"
        print(my_log)
        try: 
            my_ticker = yf.Ticker(row['Ticker'])
            my_ticker_df = my_ticker.history(start=my_start,end=my_end)
            #print(my_ticker_df)
            if not pd.isnull(my_ticker_df['Close']).all():
                my_ticker_df.to_sql(row['Ticker'], conn_data, if_exists='replace')
            else:
                print(row['Ticker'] + " has no data.")
                remaining_tickers.append(my_log)
        except Exception as e:
            # Print error message and traceback details
            remaining_tickers.append(my_log)
            print("An error occurred:")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {e}")
            traceback_details = traceback.format_exc()
            print(f"Traceback Details:\n{traceback_details}")
    print(remaining_tickers)

    print(my_tickers)
    for index,row in my_tickers.iterrows():
            try:
                print(row['Ticker'] + " " + row['Company'])
                my_stock = Stock(conn_data,row['Ticker'],row['Company'], my_start,my_end)
                if type(my_stock.stockdata["Close"].iloc[0]) == np.float64:
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
                    my_stock.stockdata["OBV"] = ta.OBV(my_stock.stockdata['Close'],my_stock.stockdata['Volume'])
                    my_stock.stockdata["RSI"] = ta.RSI(my_stock.stockdata['Close'],timeperiod=10)
                    #my_stock.stockdata["ADX"] = ta.ADX()
                    my_stock.stockdata['MACD'], my_stock.stockdata['MACDSignal'], my_stock.stockdata['MACDHist'] = ta.MACD(my_stock.stockdata['Close'], fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
                    my_stock.stockdata['ClosePercentChange'] = my_stock.stockdata['Close'].pct_change()
                    my_stock.stockdata['VolumePercentChange'] = my_stock.stockdata['Volume'].pct_change()
                    my_stock.stockdata['SMA50PercentChange'] = my_stock.stockdata['SMA50'].pct_change()

                    my_stock.stockdata['prevTEMA5'] = my_stock.stockdata['TEMA5'].shift(1)
                    my_stock.stockdata['prevTEMA20'] = my_stock.stockdata['TEMA20'].shift(1)                
                    my_stock.stockdata['prevSMA50'] = my_stock.stockdata['SMA50'].shift(1)
                    my_stock.stockdata['prevRSI'] = my_stock.stockdata['RSI'].shift(1)  
                    my_stock.stockdata['prevMACD'] = my_stock.stockdata['MACD'].shift(1)  
                    my_stock.stockdata['prevMACDSignal'] = my_stock.stockdata['MACDSignal'].shift(1)  
                    my_stock.stockdata['MACD_slope'] = np.gradient(my_stock.stockdata['MACD'], 1)
                    my_stock.stockdata['MACD_sign_change'] = np.sign(my_stock.stockdata['MACD_slope']).diff()

                    my_stock.stockdata['30'] = 30 
                    my_stock.stockdata['70'] = 70 
                    #my_stock.stockdata['RSI_position'] = RSI_position(my_stock.stockdata['RSI_X_ABOVE_30'],my_stock.stockdata['RSI_X_BELOW_70'])
                    #my_stock.stockdata['TEMA5_X_ABOVE_TEMA20'] = cross_above(my_stock.stockdata['prevTEMA5'],my_stock.stockdata['TEMA5'],my_stock.stockdata['prevTEMA20'],my_stock.stockdata['TEMA20'])
                    #my_stock.stockdata['TEMA5_X_BELOW_TEMA20'] = cross_below(my_stock.stockdata['prevTEMA5'],my_stock.stockdata['TEMA5'],my_stock.stockdata['prevTEMA20'],my_stock.stockdata['TEMA20'])

                
                    my_stock.stockdata.to_sql(row['Ticker'], conn_data, if_exists='replace', index = True)
        
            except Exception as e:
                # Get the exception information including the line number
                exc_type, exc_obj, exc_tb = sys.exc_info()
                
                # Extract the line number
                line_number = exc_tb.tb_lineno
                
                # Print the exception message along with the line number
                print(f"Exception occurred in update-stockdata on line {line_number}: {e}")
                continue


    cur_data.close()
    conn_data.close()
    cur_tickers.close()
    conn_tickers.close()

if __name__ == "__main__":
    main()