import sqlite3
import os
import pandas as pd
import numpy as np
import itertools
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import HourLocator, DayLocator, DateFormatter
import seaborn as sns
import sys

def plotgraph(conn,ticker,imagepath):
    try:
        sql_query = pd.read_sql_query("""SELECT * from '""" + ticker + """' ORDER BY Date DESC LIMIT 400""",conn)
        df = pd.DataFrame(sql_query, columns=['Date','Ticker','Adj Close','Close','High','Low','Open','Volume','Percent Change','SMA50','SMA150','SMA200','TEMA5','TEMA20','BB_low','BB_mid','BB_up','RSI'])
        print(ticker)
        print(df.iloc[-1])
        #df.set_index('Date',inplace=True)
        plt.subplot(2, 1, 1)
        plt.title(ticker)
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['Close'], color = 'cornflowerblue', label = 'Close')
        #plt.plot(pd.to_datetime(df['Date']).dt.date,df['Low'], color = 'orange', label = 'Low')
        #plt.plot(pd.to_datetime(df['Date']).dt.date,df['High'], color = 'green', label = 'High')
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['BB_low'], color = 'red', label = 'BB_low')
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['BB_mid'], color = 'purple', label = 'BB_mid')
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['BB_up'], color = 'brown', label = 'BB_up')
        plt.xticks(rotation=45)       
        plt.legend(loc="upper left")
        plt.subplot(2, 1, 2)
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['RSI'], color = 'cornflowerblue', label = 'RSI')
        plt.axhline(y=70, color='g', linestyle='-')
        plt.axhline(y=30, color='g', linestyle='-')
        plt.legend(loc="upper left")
        plt.gcf().autofmt_xdate()
        if not os.path.isdir(imagepath):
            os.makedirs(imagepath)
        plt.savefig(imagepath + "/" + ticker + "-BB.png")
        plt.clf()
            
        plt.title(ticker)
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['Close'], color = 'lightgrey', label = 'Close')
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['SMA50'], color = 'red', label = 'SMA50')
        #plt.plot(pd.to_datetime(df['Date']).dt.date,df['TEMA5'], color = 'green', label = 'TEMA5')
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['TEMA20'], color = 'cornflowerblue', label = 'TEMA20')
        plt.xticks(rotation=45)       
        plt.legend(loc="upper left")
        plt.savefig(imagepath + "/" + ticker + "-SMA.png")
        plt.clf()
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        print(exception_traceback.tb_lineno)
        print(e)
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    #plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    #plt.plot(days,200)
    #plt.gcf().autofmt_xdate()

def main():
    sns.set()

    scores = []
    gains = {}
    gains_pct = {}
    losses = {}
    losses_pct = {}
    DB_PATH = os.getenv("DB_PATH")

    now = datetime.now()
    then = now + timedelta(days=200)
    days = mdates.drange(now,then,timedelta(days=1))
    my_end = datetime.today().strftime('%Y-%m-%d')

    try:
        # DB CONNECTIONS #
        DB_PATH = os.getenv('DB_PATH')
        conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
        cur_data = conn_data.cursor()
        conn_info = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
        cur_info = conn_info.cursor()

        # Plot Portfolio stocks
        my_ticker_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE Portfolio == 1"""
        cur_info.execute(my_ticker_query)    
        my_tickers_list = cur_info.fetchall()
        my_tickers = [x[0] for x in my_tickers_list]
        for my_ticker in my_tickers:
            try:
                sql_stock = pd.read_sql_query("SELECT * from '" + my_ticker + "' WHERE Date <= '" + str(my_end) + "'",conn_data)
                my_stock_df = pd.DataFrame(sql_stock)
                if type(my_stock_df["AdjClose"].iloc[0:1][0]) == np.float64:
                    plotgraph(conn_data,my_ticker,DB_PATH + "/graphs" + "/" + datetime.today().strftime('%Y-%m-%d')) 
            except:
                print(my_ticker + ": An exception occurred")
                continue

        cur_data.close()
        conn_data.close()
        cur_info.close()
        conn_info.close()

    except Exception as e:
        print(e)
    
    
        
if __name__ == "__main__":
    main()
