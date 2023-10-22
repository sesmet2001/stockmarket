import os
import sqlite3
import yahoo_fin.stock_info as si
import pandas as pd

def main():
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/stockradar.db")

    # tickers Dow
    tickers_dow = si.tickers_dow()
    tickers_dow_df = pd.DataFrame(tickers_dow, columns=['Ticker'])
    tickers_dow_df.set_index('Ticker',inplace=True)
    tickers_dow_df.to_sql('_tickers_dow', con=conn, if_exists='replace')

    # tickers S&P500
    tickers_sp500 = si.tickers_sp500()
    tickers_sp500_df = pd.DataFrame(tickers_sp500, columns=['Ticker'])
    tickers_sp500_df.set_index('Ticker',inplace=True)
    tickers_sp500_df.to_sql('_tickers_sp500', con=conn, if_exists='replace')

    # tickers FTSE100
    tickers_ftse100 = si.tickers_ftse100()
    tickers_ftse100_df = pd.DataFrame(tickers_ftse100, columns=['Ticker'])
    tickers_ftse100_df.set_index('Ticker',inplace=True)
    tickers_ftse100_df.to_sql('_tickers_ftse100', con=conn, if_exists='replace')

    # tickers FTSE250
    tickers_ftse250 = si.tickers_ftse250()
    tickers_ftse250_df = pd.DataFrame(tickers_ftse250, columns=['Ticker'])
    tickers_ftse250_df.set_index('Ticker',inplace=True)
    tickers_ftse250_df.to_sql('_tickers_ftse250', con=conn, if_exists='replace')

    # tickers Nasdaq
    tickers_nasdaq = si.tickers_nasdaq()
    tickers_nasdaq_df = pd.DataFrame(tickers_nasdaq, columns=['Ticker'])
    tickers_nasdaq_df.set_index('Ticker',inplace=True)
    tickers_nasdaq_df.to_sql('_tickers_nasdaq', con=conn, if_exists='replace')
    
    # tickers Other
    tickers_other = si.tickers_other()
    tickers_other_df = pd.DataFrame(tickers_other, columns=['Ticker'])
    tickers_other_df.set_index('Ticker',inplace=True)
    tickers_other_df.to_sql('_tickers_other', con=conn, if_exists='replace')

    conn.close()

if __name__ == "__main__":
    main()
