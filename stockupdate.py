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

def main():

    # Main parameters
    debug = 1
    ticker_limit = 100 
    chunksize = 100
    
    # Technical Analysis
    SMA_FAST = 50
    SMA_SLOW = 200
    RSI_PERIOD = 14
    RSI_AVG_PERIOD = 15
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    STOCH_K = 14
    STOCH_D = 3
    SIGNAL_TOL = 3
    Y_AXIS_SIZE = 12    

    yf.pdr_override() 
    
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/stockradar.db")

    cur = conn.cursor()

    ############ DEFINE START END #########
    #sqldates = "SELECT Date FROM AAPL ORDER BY date DESC LIMIT 1"
    #start = cur.execute(sqldates).fetchone()
    start = None
    if start == None:
        start = datetime(2021, 1, 1)
    else:
        start = datetime.strptime(start[0], '%Y-%m-%d %H:%M:%S')
        start = start.date() + timedelta(days=2)
    end = datetime.today().strftime('%Y-%m-%d')
    #end = "2021-09-01"

    ############ LOAD TICKERS ############
    sqltickers = """SELECT Ticker FROM _tickers_sp500"""
    # sqltickers = """SELECT Ticker FROM _watchlist 
    # UNION SELECT Ticker FROM _portfolio 
    # UNION SELECT Ticker FROM _tickers_dow 
    # UNION SELECT Ticker FROM _tickers_sp500
    # UNION SELECT Ticker FROM _tickers_nasdaq"""
    # UNION SELECT Ticker FROM _tickers_ftse100
    # UNION SELECT Ticker FROM _tickers_ftse250
    # UNION SELECT Ticker FROM _tickers_euronext
    # UNION SELECT Ticker FROM _tickers_other"""
    
    #sqlsymbols = """SELECT Symbol FROM _symbols_sp500 UNION SELECT ticker FROM _tickers_sp500 UNION SELECT ticker FROM _tickers_other"""
    #sqltickers = """SELECT ticker FROM _tickers_sp500"""
    #sqlsymbols = """SELECT Symbol FROM _symbols_sp500 WHERE Symbol='AAPL'"""
    #sqltickers = """SELECT ticker FROM _tickers"""
    cur.execute(sqltickers)
    tickers = cur.fetchall()
    #symbols = [x[0] + x[1] for x in symbols]
    tickers = [x[0] for x in tickers]

    ## in chunks
    chunks = [tickers[i:i + chunksize] for i in range(0, len(tickers), chunksize)]
    try:
        for chunk in chunks:
            print(str(chunk) + "\n")
            data = yf.download(" ".join(chunk),start=start,end=end,actions=False)
            for ticker in chunk:
                #print(symbol)
                ticker_df = data.loc[:,[("Adj Close",ticker),("Close",ticker),("High",ticker),("Low",ticker),("Open",ticker),("Volume",ticker)]]
                ticker_df.columns = ["AdjClose","Close","High","Low","Open","Volume"]
                ticker_df["Symbol"] = ticker
                #print(symboldf.shape[0])
                if not pd.isnull(ticker_df['AdjClose']).all():
                    ticker_df.to_sql(ticker, conn, if_exists='replace')
                else:
                    print(ticker + " has no data.")

    except Exception as ex:
        print(ex)
        pass

    for ticker in tickers:
        try:
            #print("TA -" + symbol)
            #sql_query = pd.read_sql_query("""SELECT * from '""" + symbol + """' ORDER BY Date""",conn)
            #df = pd.DataFrame(sql_query, columns=["Symbol","Date","AdjClose","Close","High","Low","Open","Volume"])
            #my_stock = Stock(symbol, df)
            my_stock = Stock(ticker, end)
            if type(my_stock.getQuotes()["AdjClose"].iloc[0:1][0]) == np.float64:
                my_stock.dropna()
                my_stock.BBands()
                my_stock.SMA(10)
                my_stock.SMA(50)
                my_stock.SMA(150)
                my_stock.SMA(200)
                my_stock.TEMA(5)
                my_stock.TEMA(10)
                my_stock.TEMA(20)   
                my_stock.TEMA(50)   
                my_stock.RSI()
                my_stock.MACD(MACD_FAST,MACD_SLOW,MACD_SIGNAL)
                my_stock.Close_pct_change()
                my_stock.Volume_pct_change()
                my_stock.SMA50_pct_change()
                my_stock.df.to_sql(ticker, conn, if_exists='replace', index = False)
        except:
            print(ticker + ": An exception occurred")
            continue

    cur.close()
    conn.close()

if __name__ == "__main__":
    print(timeit.timeit(main,number=1))