from base.stock import Stock
import sqlite3
import os
import pandas as pd
import numpy as np
from indicators.volume import Volume
from indicators.bbands import BBands
import itertools
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import HourLocator, DayLocator, DateFormatter
import seaborn as sns

def main():
    sns.set()
    DB_PATH = os.getenv("DB_PATH")

    try:
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        cur = conn.cursor()
    except Exception as e:
        print(e)

    sql_tickers = """select Ticker from _signals WHERE buy_SMAClose=1"""

    #sql_tickers = """SELECT ticker FROM tickers_nasdaq WHERE ticker = 'AAPL' OR ticker = 'GOOG' OR ticker='NFLX' OR ticker='TLRY'"""

    tickers = cur.execute(sql_tickers).fetchall()
    tickers = [x[0] for x in tickers]

    now = datetime.now()
    then = now + timedelta(days=200)
    days = mdates.drange(now,then,timedelta(days=1))

    scores = []
    gains = {}
    gains_pct = {}
    losses = {}
    losses_pct = {}
    dir_wamp = "/var/www/destef_be"
    dir_portfolio = dir_wamp + "/buyradar" + "/" + datetime.today().strftime('%Y-%m-%d')

    for ticker in tickers:
        sql_query = pd.read_sql_query("""SELECT * from '""" + ticker + """' ORDER BY Date DESC LIMIT 100""",conn)
        df = pd.DataFrame(sql_query, columns=['Date','Ticker','Adj Close','Close','High','Low','Open','Volume','Percent Change','SMA50','SMA150','SMA200','BB_low','BB_mid','BB_up','RSI'])#.tail(50)
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
        if not os.path.isdir(dir_portfolio):
            os.makedirs(dir_portfolio)
        plt.savefig(dir_portfolio + "/" + ticker + "-BB.png")
        plt.clf()
        

        plt.title(ticker)
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['Close'], color = 'cornflowerblue', label = 'Close')
        plt.plot(pd.to_datetime(df['Date']).dt.date,df['SMA50'], color = 'orange', label = 'SMA50')
        #plt.plot(pd.to_datetime(df['Date']).dt.date,df['SMA150'], color = 'green', label = 'SMA150')
        #plt.plot(pd.to_datetime(df['Date']).dt.date,df['SMA200'], color = 'red', label = 'SMA200')
        plt.xticks(rotation=45)       
        plt.legend(loc="upper left")
        plt.savefig(dir_portfolio + "/" + ticker + "-SMA.png")
        plt.clf()
        
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        #plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
        #plt.plot(days,200)
        #plt.gcf().autofmt_xdate()
        
if __name__ == "__main__":
    main()
