import yfinance as yf
import sqlite3
import os
import pandas as pd
import numpy as np
import itertools
from datetime import date, datetime, timedelta
from collections import defaultdict

def main():
    DB_PATH = os.getenv('DB_PATH')
    
    try:
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        cur = conn.cursor()
    except Exception as e:
        print(e)

    with open('delete_tickers.txt') as f:
        for ticker in f:
            try:
                print(ticker)
                sql_delete = """DELETE FROM _symbols_nasdaq WHERE symbol = '""" + ticker.rstrip() + """'"""
                cur.execute(sql_delete)
                # sql_delete = """DELETE FROM _tickers_nasdaq WHERE ticker = '""" + ticker.rstrip() + """'"""
                # cur.execute(sql_delete)
                # sql_delete = """DELETE FROM _tickers_sp500 WHERE ticker = '""" + ticker.rstrip() + """'"""
                # cur.execute(sql_delete)
                # sql_delete = """DELETE FROM _tickers_other WHERE ticker = '""" + ticker.rstrip() + """'"""
                # cur.execute(sql_delete)
                conn.commit()
            except Exception as e:
                print(e)
    conn.close()
        
if __name__ == "__main__":
    main()