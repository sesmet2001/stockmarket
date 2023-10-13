import yfinance as yf
import pandas as pd
import sqlite3
import os

def main():
    DB_PATH = os.getenv('DB_PATH')
    yf.pdr_override()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    financials_df = pd.DataFrame()

    conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
    cur = conn.cursor()

    sqlsymbols = """SELECT Ticker FROM _yahoo_fin_tickers LIMIT 5"""

    my_tickers = cur.execute(sqlsymbols).fetchall()
    my_tickers = [x[0] for x in my_tickers]
    for my_ticker in my_tickers:
        print(my_ticker)
        my_stock = yf.Ticker(my_ticker)
        my_stock_info_dict = my_stock.info
        my_stock_info_df = pd.DataFrame.from_dict(my_stock_info_dict, orient="index")
        my_stock_info_df = my_stock_info_df.transpose()
        my_stock_info_df['Symbol'] = my_ticker
        my_stock_info_df.set_index(['Symbol'], append=True, inplace=True)
        my_stock_info_df.reset_index(inplace=True)
        financials_df = pd.concat([financials_df,my_stock_info_df])
    print(financials_df)

if __name__ == "__main__":
    main()