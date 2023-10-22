# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 10:38:25 2021

@author: sefsmet
"""

import bt
import pandas as pd
import os
import sqlite3
import matplotlib.pyplot as plt
from base.strategy import Strategy



def main():
    try:
        conn = sqlite3.connect("/tmp/stockradar.db")
        cur = conn.cursor()
    except Exception as e:
        print(e)

    start_date = "2022-04-01"
    end_date = "2022-04-15"
    daterange = pd.date_range(start_date, end_date)
    my_strategy = Strategy()

    for single_date in daterange:

        print(single_date.strftime("%Y-%m-%d"))


    price_data = pd.read_sql_query("SELECT * from AAPL WHERE Date > '" + start_date + "'", conn)
    df = pd.DataFrame(price_data)
    print(df)

    #price_data = bt.get('aapl', start='2019-11-1')
    #print(type(price_data))
    #price_data = pd.read_sql_query("SELECT * from AAPL WHERE Date < '2020-09-12' AND Date > '2020-07-12'", conn)
    #print(price_data.head())
    #sma =  talib.SMA(price_data['Close'], timeperiod=20)
    #sma = price_data.rolling(20).mean()
    #print(sma)
    #bt_strategy = bt.Strategy('AboveSMA',
    #                           [bt.algos.SelectWhere(price_data > sma),
    #                            bt.algos.WeighEqually(),
    #                            bt.algos.Rebalance()])

    #bt_backtest = bt.Backtest(bt_strategy, price_data)
    #bt_result = bt.run(bt_backtest)
    #bt_result.plot(title='Backtest result')
    #plt.show()
    #bt_result.display()


if __name__ == "__main__":
    main()