import pandas as pd
from datetime import datetime, timedelta
import timeit
import numpy as np
import sqlite3
import yahoo_fin.stock_info as si
import os

def main():
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/stockradar.db")
    cur = conn.cursor()
        
    sqlsymbols = """SELECT Symbol FROM _symbols_euronext UNION SELECT Symbol FROM _symbols_nasdaq UNION SELECT Symbol FROM _symbols_sp500 LIMIT 5"""

    tickers = cur.execute(sqlsymbols).fetchall()
    tickers = [x[0] for x in tickers]
    
    for ticker in tickers:
        print(ticker)
        try:
            print(si.get_next_earnings_date(ticker))
        except Exception as e:
            print(e)
            pass
        #.to_sql('_yahoo_fin_earnings', con=conn, if_exists='append')
    conn.close()

if __name__ == "__main__":
    print(timeit.timeit(main,number=1))
