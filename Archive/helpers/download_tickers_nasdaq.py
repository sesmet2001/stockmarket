import os
import sqlite3
import yahoo_fin.stock_info as si
import pandas as pd

def main():
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/stockradar.db")
    
    # tickers Nasdaq
    tickers_nasdaq = si.tickers_nasdaq()
    tickers_nasdaq_df = pd.DataFrame(tickers_nasdaq, columns=['Symbol'])
    tickers_nasdaq_df.set_index('Symbol',inplace=True)
    tickers_nasdaq_df.to_sql('_tickers_nasdaq', con=conn, if_exists='replace')
    #si.get_day_most_active().to_sql('_yahoo_fin_day_most_active', con=conn, if_exists='replace')
    conn.close()

if __name__ == "__main__":
    main()
