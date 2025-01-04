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

def cross_above_function(prev_val1,cur_val1,prev_val2,cur_val2):
    try:
        #print("prev_val1: " + str(prev_val1) + ", cur_val1: " + str(cur_val1) + ", cur_val2: " + str(cur_val2))
        if not (np.isnan(prev_val1) or np.isnan(cur_val1) or np.isnan(prev_val2) or np.isnan(cur_val2)):
            if prev_val1 < prev_val2 and cur_val1 > cur_val2:
                return True
            else:
                return False       
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Exception occurred in cross on line {line_number}: {e}")

def cross_below_function(prev_val1,cur_val1,prev_val2,cur_val2):
    try:
        #print("prev_val1: " + str(prev_val1) + ", cur_val1: " + str(cur_val1) + ", cur_val2: " + str(cur_val2))
        if not (np.isnan(prev_val1) or np.isnan(cur_val1) or np.isnan(prev_val2) or np.isnan(cur_val2)):
            if prev_val1 > prev_val2 and cur_val1 < cur_val2:
                return True
            else:
                return False     
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Exception occurred in cross on line {line_number}: {e}")

def detect_trend_changes(series):
    """
    Detects trend changes in a pandas Series.
    A trend change is defined when the direction of the curve changes (from increasing to decreasing or vice versa).

    Parameters:
    series (pd.Series): The pandas Series containing the curve values.

    Returns:
    pd.Series: A series of the same length, where 1 indicates an upward trend change (from decreasing to increasing),
               -1 indicates a downward trend change (from increasing to decreasing), and 0 indicates no change.
    """
    #Calculate the first difference (discrete derivative)
    diff = series.diff()

    # Detect where the sign of the derivative changes
    trend_change = np.sign(diff).diff()

    # Map changes to -1 for downward change, 1 for upward change, and 0 for no change
    trend_change = trend_change.map({-2: 1, 2: -1}).fillna(0)
    
    return trend_change


def main():
    
    
    # PARAMETERS #
    chunksize = 100
    max_retries = 3
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    my_plotrange = 100
    my_start = datetime(2021, 1, 1)
    my_strategy = "X_TEMA5_TEMA20"
    #yf.pdr_override() 
    cross_above = np.vectorize(cross_above_function)
    cross_below = np.vectorize(cross_below_function)
    print(sys.path)
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


    # LOAD TICKER DATA #
    #my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE SP500 == 1 OR Dow == 1 OR Portfolio == 1 OR Crypto == 1 OR PreciousMetals == 1 OR Oil == 1 OR ExchangeRates == 1"""
    my_ticker_types = ["Beursrally","Portfolio","ExchangeRates","Oil","Crypto","PreciousMetals","Other","Dow","SP500","Screener","Nasdaq"]
    
    for my_ticker_type in my_ticker_types:
        my_ticker_query = 'SELECT Ticker, Company FROM _yahoo_fin_tickers WHERE ' + my_ticker_type + ' == 1'    
        my_tickers = pd.read_sql(my_ticker_query, conn_tickers)
        my_tickers['Ticker'] = my_tickers['Ticker'].replace('BRK.A', 'BRK-A')
        my_tickers['Ticker'] = my_tickers['Ticker'].replace('PBR.A', 'PBR-A')
        my_tickers['Ticker'] = my_tickers['Ticker'].replace('LEN.B', 'LEN-B')
        my_tickers['Ticker'] = my_tickers['Ticker'].replace('HEI.A', 'HEI-A')
        my_tickers['Ticker'] = my_tickers['Ticker'].replace('VUSA.AS', 'VUSA-AS')
        my_tickers.set_index('Ticker', inplace=True)

        # DOWNLOAD DATA IN CHUNKS #
        #print("Number of tickers: " + str(len(my_tickers[0])))
        print("Stock data from " + str(my_start) + " until " + str(my_end))
        chunks = [my_tickers[i:i + chunksize].index for i in range(0, len(my_tickers), chunksize)]
        #print("chunks: " + str(chunks))
        for chunk in chunks:
            retry_tickers = []
            #print(str(chunk) + "\n")
            print(" ".join(chunk))
            retry_count = 0
    

            try:
                data = yf.download(" ".join(chunk),start=my_start,end=my_end,actions=False,)
                #break
                #print(data)
            except Exception as e:          
                # Print the exception message along with the line number
                print(f"Exception occurred on line {line_number}: {e}")
                retry_count += 1
                print(f"Error with {chunk}, retry {retry_count}: {e}")
                time.sleep(5)  # Wait before retrying


            #print(data.describe())
            #print(chunk)
            #print(data)
            for my_ticker in chunk:
                my_ticker_df = data.loc[:,[("Adj Close",my_ticker),("Close",my_ticker),("High",my_ticker),("Low",my_ticker),("Open",my_ticker),("Volume",my_ticker)]]
                my_ticker_df.columns = ["AdjClose","Close","High","Low","Open","Volume"]
                #my_ticker_df["Ticker"] = my_ticker
                if not pd.isnull(my_ticker_df['AdjClose']).all():
                    my_ticker_df.to_sql(my_ticker, conn_data, if_exists='replace')
                else:
                    print(my_ticker + " has no data.")
                    chunk.append(my_ticker)
            #time.sleep(1)
            try:
                data = yf.download(" ".join(retry_tickers),start=my_start,end=my_end,actions=False,)
                #break
                #print(data)
            except Exception as e:          
                # Print the exception message along with the line number
                print(f"Exception occurred on line {line_number}: {e}")
                retry_count += 1
                print(f"Error with {chunk}, retry {retry_count}: {e}")
                time.sleep(5)  # Wait before retrying       

        
        
        #print(my_tickers.iterrows())
        #print("Calculate Features:")
        for my_ticker,my_company in my_tickers.iterrows():
            try:
                print(my_ticker + " " + my_company)
                my_stock = Stock(conn_data,my_ticker,my_company, my_start,my_end)
                if type(my_stock.stockdata["AdjClose"].iloc[0]) == np.float64:
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
                    my_stock.stockdata['ClosePercentChange'] = my_stock.stockdata['AdjClose'].pct_change()
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
                    my_stock.stockdata['RSI_XABOVE_30'] = cross_above(my_stock.stockdata['prevRSI'],my_stock.stockdata["RSI"],my_stock.stockdata['30'],my_stock.stockdata['30'])
                    my_stock.stockdata['RSI_XBELOW_70'] = cross_below(my_stock.stockdata['prevRSI'],my_stock.stockdata["RSI"],my_stock.stockdata['70'],my_stock.stockdata['70'])
                    #my_stock.stockdata['RSI_position'] = RSI_position(my_stock.stockdata['RSI_X_ABOVE_30'],my_stock.stockdata['RSI_X_BELOW_70'])
                    #my_stock.stockdata['TEMA5_X_ABOVE_TEMA20'] = cross_above(my_stock.stockdata['prevTEMA5'],my_stock.stockdata['TEMA5'],my_stock.stockdata['prevTEMA20'],my_stock.stockdata['TEMA20'])
                    #my_stock.stockdata['TEMA5_X_BELOW_TEMA20'] = cross_below(my_stock.stockdata['prevTEMA5'],my_stock.stockdata['TEMA5'],my_stock.stockdata['prevTEMA20'],my_stock.stockdata['TEMA20'])
                    my_stock.stockdata['MACD_X_ABOVE_MACDSignal'] = cross_above(my_stock.stockdata['prevMACD'],my_stock.stockdata['MACD'],my_stock.stockdata['prevMACDSignal'],my_stock.stockdata['MACDSignal'])
                    my_stock.stockdata['MACD_X_BELOW_MACDSignal'] = cross_below(my_stock.stockdata['prevMACD'],my_stock.stockdata['MACD'],my_stock.stockdata['prevMACDSignal'],my_stock.stockdata['MACDSignal'])
                
                    my_stock.stockdata.to_sql(my_ticker, conn_data, if_exists='replace', index = True)
        
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