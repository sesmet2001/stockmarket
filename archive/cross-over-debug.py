from pandas_datareader.data import DataReader
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import timeit
import sqlite3
import numpy as np
import sqlite3
import os
import sys
import talib.abstract as ta
import socket
import traceback
import vectorbt as vbt
from backtesting.lib import crossover
import warnings

def main():
    # DB CONNECTIONS #
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")

    df = pd.read_sql_query("SELECT * from CSCO WHERE TEMA5_X_ABOVE_TEMA20==1",conn)
    print(df[['Date','prevTEMA5','prevTEMA20','TEMA5','TEMA20','TEMA5_X_ABOVE_TEMA20']])
    conn.close()

if __name__ == "__main__":
    main()