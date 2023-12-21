from stock import Stock
import sqlite3
import pandas as pd
import numpy as np

def main():
    try:
        conn = sqlite3.connect('../stockmon.db')
        cur = conn.cursor()
    except Exception as e:
        print(e.message)

    sql_tickers = """SELECT ticker FROM tickers_euronext
    UNION SELECT ticker FROM tickers_nasdaq
    UNION SELECT ticker FROM tickers_sp500 
    UNION SELECT ticker FROM tickers_other"""

    tickers = cur.execute(sql_tickers).fetchall()
    tickers = [x[0] for x in tickers]

    for ticker in tickers:
        sql_stock = pd.read_sql_query("""SELECT * FROM """ + ticker + """""",conn)
        stockdf = pd.DataFrame(sql_stock, columns=['Adj Close','Close','High','Low','Open','Volume'])
        my_stock = Stock(ticker,stockdf)
        #print(ticker)
        #print(type(my_stock.getData()['Adj Close'].iloc[0:1][0]))
        if type(my_stock.getData()['Adj Close'].iloc[0:1][0]) == np.float64:
            today = float(my_stock.getQuotes()['Adj Close'].iloc[0:1])
            yesterday = float(my_stock.getQuotes()['Adj Close'].iloc[1:2])
            diff = (today - yesterday) / today
            #print(str(diff) + " " + ticker)
            if diff > 0.3:
                print(str(diff) + " " + ticker)
            #print(my_stock.getEMA(10))

if __name__ == "__main__":
    main()
