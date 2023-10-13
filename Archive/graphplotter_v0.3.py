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
import sys

def plotgraphs(conn,tickers,imagepath):
    for ticker in tickers:
        try:
            sql_query = pd.read_sql_query("""SELECT * from '""" + ticker + """' ORDER BY Date DESC""",conn)
            df = pd.DataFrame(sql_query, columns=['Date','Ticker','Adj Close','Close','High','Low','Open','Volume','Percent Change','SMA50','SMA150','SMA200','TEMA5','TEMA20','BB_low','BB_mid','BB_up','RSI'])#.tail(50)
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

    try:
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        cur = conn.cursor()


        # watchlist netincome
        sql_tickers = """SELECT * FROM _yf_financials_netincome_scores WHERE `Net Income` > 1000000 ORDER BY NetIncomePctChange DESC LIMIT 100"""
        tickers = cur.execute(sql_tickers).fetchall()
        print(tickers)
        tickers = [x[3] for x in tickers]
        dir_watchlist = DB_PATH + "/graphs" + "/" + datetime.today().strftime('%Y-%m-%d')
        plotgraphs(conn,tickers,dir_watchlist)
        
        # watchlist totalrevenue
        sql_tickers = """SELECT * FROM _yf_financials_revenue_scores WHERE `Total Revenue` > 1000000 ORDER BY RevenuePctChange DESC LIMIT 100"""
        tickers = cur.execute(sql_tickers).fetchall()
        tickers = [x[2] for x in tickers]
        dir_watchlist = DB_PATH + "/graphs" + "/" + datetime.today().strftime('%Y-%m-%d')
        plotgraphs(conn,tickers,dir_watchlist)
    
    
        # watchlist graphs
        sql_tickers = """select Ticker from _watchlist"""
        
        tickers = cur.execute(sql_tickers).fetchall()
        tickers = [x[0] for x in tickers]
        dir_watchlist = DB_PATH + "/graphs/" + datetime.today().strftime('%Y-%m-%d')
        plotgraphs(conn,tickers,dir_watchlist)
    
        # portfolio graphs
        sql_tickers = """select Ticker from _portfolio"""
        tickers = cur.execute(sql_tickers).fetchall()
        tickers = [x[0] for x in tickers]
        dir_portfolio = DB_PATH + "/graphs" + "/" + datetime.today().strftime('%Y-%m-%d')
        plotgraphs(conn,tickers,dir_portfolio)
    
        # buy_radar graphs
        sql_tickers = """select Ticker from _signals WHERE buy_SMACrossClose=1"""
        tickers = cur.execute(sql_tickers).fetchall()
        tickers = [x[0] for x in tickers]
        dir_buyradar = DB_PATH + "/graphs" + "/" + datetime.today().strftime('%Y-%m-%d')
        plotgraphs(conn,tickers,dir_buyradar)
    except Exception as e:
        print(e)
    
    
        
if __name__ == "__main__":
    main()
