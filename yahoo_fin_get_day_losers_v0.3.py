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
    si.get_day_losers().to_sql('_yahoo_fin_day_losers', con=conn, if_exists='replace')
    conn.close()

if __name__ == "__main__":
    print(timeit.timeit(main,number=1))
