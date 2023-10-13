from pandas_datareader.data import DataReader
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import timeit
import sqlite3
from base.stock import Stock
from indicators.volume import Volume
from indicators.bbands import BBands
import numpy as np
import sqlite3
import os
from yahoo_fin.stock_info import *
import mysql.connector as mysql
from sqlalchemy.types import Integer, Text, String, DateTime

def get_financials(tickers):
    financials_df = pd.DataFrame()
    for ticker in tickers:
        print(ticker)
        try:
            my_ticker = yf.Ticker(ticker)
            my_ticker_financials = my_ticker.financials
            if not my_ticker_financials.empty:
                my_ticker_financials_df = my_ticker_financials.transpose()
                my_ticker_financials_df['Symbol'] = ticker 
                my_ticker_financials_df.set_index(['Symbol'], append=True, inplace=True)
                financials_df = financials_df.append(my_ticker_financials_df)
        except Exception as e:
            print(e)
            pass
    return financials_df

def main():
    yf.pdr_override()     
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/stockradar.db")
    cur = conn.cursor()
 
    # income info
    sqltickers = """SELECT Symbol FROM _yf_financials_netincome_scores WHERE `Net Income` > 1000000 ORDER BY NetIncomePctChange DESC LIMIT 100"""
    cur.execute(sqltickers)
    tickers = cur.fetchall()
    tickers = [x[0] for x in tickers]
    get_financials(tickers).to_sql('_yf_financials', conn, if_exists='replace',index_label=['Date','Symbol'])

    # # revenue info
    sqltickers = """SELECT Symbol FROM _yf_financials_revenue_scores WHERE `Total Revenue` > 1000000 ORDER BY RevenuePctChange DESC LIMIT 100"""
    cur.execute(sqltickers)
    tickers = cur.fetchall()
    tickers = [x[0] for x in tickers]
    get_financials(tickers).to_sql('_yf_financials', conn, if_exists='append',index_label=['Date','Symbol'])

    # # watchlist info
    sqltickers = """select Ticker from _watchlist"""
    cur.execute(sqltickers)
    tickers = cur.fetchall()
    tickers = [x[0] for x in tickers]
    get_financials(tickers).to_sql('_yf_financials', conn, if_exists='append',index_label=['Date','Symbol']) 
    
    # portfolio info
    sqltickers = """select Ticker from _portfolio"""
    cur.execute(sqltickers)
    tickers = cur.fetchall()
    tickers = [x[0] for x in tickers]
    get_financials(tickers).to_sql('_yf_financials', conn, if_exists='append',index_label=['Date','Symbol'])  

    # buy_radar info
    sqltickers = """select Ticker from _signals WHERE buy_SMACrossClose=1"""
    cur.execute(sqltickers)
    tickers = cur.fetchall()
    tickers = [x[0] for x in tickers]
    get_financials(tickers).to_sql('_yf_financials', conn, if_exists='append',index_label=['Date','Symbol'])
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    print(timeit.timeit(main,number=1))
