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

def main():
    # PARAMETERS #
    chunksize = 100
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    my_plotrange = 100
    my_strategy = "X_TEMA5_TEMA20"
    yf.pdr_override() 
    cross_above = np.vectorize(cross_above_function)
    cross_below = np.vectorize(cross_below_function)
    print(sys.path)
    pd.set_option('display.max_rows', None)
    
    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-rrndata.db")
    cur_data = conn_data.cursor()
    conn_info = sqlite3.connect(DB_PATH + "/database/stockradar-lite.db")
    cur_info = conn_info.cursor()

    my_start = datetime(2016, 1, 1)
    my_end = datetime.today().strftime('%Y-%m-%d')
    #my_end = datetime.strptime("2023-10-13", '%Y-%m-%d')
    print(my_start)
    print(my_end)

    # LOAD TICKER DATA #
    # test
    # my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR PreciousMetals == 1 OR Crypto == 1 OR Portfolio == 1"""
    my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Dow == 1 OR Portfolio == 1 OR Crypto == 1 OR PreciousMetals == 1 OR Oil == 1 OR ExchangeRates == 1"""
    #my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Portfolio == 1"""
    cur_info.execute(my_ticker_query)    
    my_tickers_list = cur_info.fetchall()
    my_tickers = [x[0] for x in my_tickers_list]
    #my_tickers = ["MSFT","NVDA"]


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
        # Get the exception information including the line number
        exc_type, exc_obj, exc_tb = sys.exc_info()
        
        # Extract the line number
        line_number = exc_tb.tb_lineno
        
        # Print the exception message along with the line number
        print(f"Exception occurred on line {line_number}: {e}")
        pass
    
    for my_ticker in my_tickers:
        try:
            my_stock = Stock(conn_data,my_ticker,my_start,my_end)
            if type(my_stock.stockdata["AdjClose"].iloc[0]) == np.float64:
                print(my_stock.ticker)
                my_stock.dropna()
                #print(my_stock.stockdata["SL_Price"].tail(10))
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
                my_stock.stockdata["RSI"] = ta.RSI(my_stock.stockdata['Close'],timeperiod=6)
                my_stock.stockdata['MACD'], my_stock.stockdata['MACDSignal'], my_stock.stockdata['MACDHist'] = ta.MACD(my_stock.stockdata['Close'], fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
                my_stock.stockdata['ClosePercentChange'] = my_stock.stockdata['AdjClose'].pct_change()
                my_stock.stockdata['VolumePercentChange'] = my_stock.stockdata['Volume'].pct_change()
                my_stock.stockdata['SMA50PercentChange'] = my_stock.stockdata['SMA50'].pct_change()
                my_stock.stockdata['ClosePercentChange'] = my_stock.stockdata['AdjClose'].pct_change()
                my_stock.stockdata['prevTEMA5'] = my_stock.stockdata['TEMA5'].shift(1)
                my_stock.stockdata['prevTEMA20'] = my_stock.stockdata['TEMA20'].shift(1)                
                my_stock.stockdata['prevSMA50'] = my_stock.stockdata['SMA50'].shift(1)
                my_stock.stockdata['prevRSI'] = my_stock.stockdata['RSI'].shift(1)  
                my_stock.stockdata['prevMACD'] = my_stock.stockdata['MACD'].shift(1)  
                my_stock.stockdata['prevMACDSignal'] = my_stock.stockdata['MACDSignal'].shift(1)  
                my_stock.stockdata['RSI_X_ABOVE_30'] = cross_above(my_stock.stockdata['prevRSI'],my_stock.stockdata["RSI"],30,30)
                my_stock.stockdata['RSI_X_BELOW_70'] = cross_below(my_stock.stockdata['prevRSI'],my_stock.stockdata["RSI"],70,70)
                #my_stock.stockdata['RSI_position'] = RSI_position(my_stock.stockdata['RSI_X_ABOVE_30'],my_stock.stockdata['RSI_X_BELOW_70'])
                my_stock.stockdata['TEMA5_X_ABOVE_TEMA20'] = cross_above(my_stock.stockdata['prevTEMA5'],my_stock.stockdata['TEMA5'],my_stock.stockdata['prevTEMA20'],my_stock.stockdata['TEMA20'])
                my_stock.stockdata['TEMA5_X_BELOW_TEMA20'] = cross_below(my_stock.stockdata['prevTEMA5'],my_stock.stockdata['TEMA5'],my_stock.stockdata['prevTEMA20'],my_stock.stockdata['TEMA20'])
                my_stock.stockdata['MACD_X_ABOVE_MACDSignal'] = cross_above(my_stock.stockdata['prevMACD'],my_stock.stockdata['MACD'],my_stock.stockdata['prevMACDSignal'],my_stock.stockdata['MACDSignal'])
                my_stock.stockdata['MACD_X_BELOW_MACDSignal'] = cross_below(my_stock.stockdata['prevMACD'],my_stock.stockdata['MACD'],my_stock.stockdata['prevMACDSignal'],my_stock.stockdata['MACDSignal'])
                my_stock.stockdata['RSI_ABOVE_50'] = np.where(my_stock.stockdata['RSI'] > 50, True, False)
                my_stock.stockdata['RSI_BELOW_50'] = np.where(my_stock.stockdata['RSI'] < 50, True, False)
                my_stock.stockdata['RSI_ABOVE_70'] = np.where(my_stock.stockdata['RSI'] > 70, True, False)
                my_stock.stockdata['RSI_BELOW_70'] = np.where(my_stock.stockdata['RSI'] < 70, True, False)
                my_stock.stockdata['RSI_BELOW_30'] = np.where(my_stock.stockdata['RSI'] < 30, True, False)
                my_stock.stockdata['RSI_ABOVE_30'] = np.where(my_stock.stockdata['RSI'] > 30, True, False)
                my_stock.stockdata['TEMA5_ABOVE_TEMA20'] = np.where(my_stock.stockdata['TEMA5'] > my_stock.stockdata['TEMA20'], True, False)
                my_stock.stockdata['TEMA5_BELOW_TEMA20'] = np.where(my_stock.stockdata['TEMA5'] < my_stock.stockdata['TEMA20'], True, False)
                my_stock.stockdata['TEMA20_ABOVE_SMA50'] = np.where(my_stock.stockdata['TEMA20'] > my_stock.stockdata['SMA50'], True, False)
                my_stock.stockdata['TEMA20_BELOW_SMA50'] = np.where(my_stock.stockdata['TEMA20'] < my_stock.stockdata['SMA50'], True, False)
                my_stock.stockdata['MACD_ABOVE_MACDSignal'] = np.where(my_stock.stockdata['MACD'] > my_stock.stockdata['MACDSignal'], True, False)
                my_stock.stockdata['MACD_BELOW_MACDSignal'] = np.where(my_stock.stockdata['MACD'] < my_stock.stockdata['MACDSignal'], True, False)
                #my_stock.stockdata['curBuy'] = my_stock.stockdata['RSI_X_ABOVE_30'] + my_stock.stockdata['TEMA5_X_ABOVE_TEMA20'] #+ my_stock.stockdata['MACD_X_ABOVE_MACDSignal'] 
                #my_stock.stockdata['Buy'] = my_stock.stockdata['curBuy'].rolling(6, min_periods=1).sum()
                #my_stock.stockdata['curSell'] = my_stock.stockdata['RSI_X_BELOW_70'] + my_stock.stockdata['TEMA5_X_BELOW_TEMA20'] #+ my_stock.stockdata['MACD_X_BELOW_MACDSignal']
                #my_stock.stockdata['Sell'] = my_stock.stockdata['curSell'].rolling(6, min_periods=1).sum()
                #my_stock.stockdata['Buy'] = my_stock.stockdata[['RSI_X_ABOVE_30','TEMA5_X_ABOVE_TEMA20','MACD_X_ABOVE_MACDSignal']].all()
                #my_stock.stockdata['Sell'] = my_stock.stockdata[['RSI_X_BELOW_70','TEMA5_X_BELOW_TEMA20','MACD_X_BELOW_MACDSignal']].all()
                #my_stock.stockdata['TEMA5_X_BELOW_TEMA20'] = np.where(my_stock.stockdata['TEMA5'] < my_stock.stockdata['TEMA20'], 1, 0)
                #my_stock.stockdata['TEMA5_X_ABOVE_TEMA20'] = crossover(my_stock.stockdata['TEMA5'], my_stock.stockdata['TEMA20'])
                #my_stock.stockdata['X_TEMA5_TEMA20'] = Cross(my_stock,"TEMA5","TEMA20").detect()
                #my_stock.stockdata.dropna(inplace=True)
                #my_stock.stockdata['TEMA20_SMA50_crossover'] = np.vectorize(find_TEMA20_SMA50_crossover)(my_stock.stockdata["prevTEMA20"],my_stock.stockdata["TEMA20"],my_stock.stockdata["prevSMA50"],my_stock.stockdata["SMA50"])     
                #my_stock.stockdata['TEMA5_TEMA20'] = np.vectorize(TEMA5_TEMA20_crossover)(my_stock.stockdata["prevTEMA5"],my_stock.stockdata["TEMA5"],my_stock.stockdata["prevTEMA20"],my_stock.stockdata["TEMA20"])            
                #print(my_stock.stockdata["SL_Price"].tail(10))
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
    cur_info.close()
    conn_info.close()

if __name__ == "__main__":
    main()