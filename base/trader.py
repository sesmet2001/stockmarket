# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:23:53 2021

@author: sefsmet
"""

import talib.abstract as ta
import pandas as pd
from base.stock import Stock
import sqlite3
import os

class Trader():
    
    def __init__(self, Portfolio, Balance):
        self.portfolio = Portfolio 
        self.balance = Balance

    def buy(self,my_stock,my_amount,my_date):
        DB_PATH = os.getenv("DB_PATH")
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        cursor = conn.cursor()
        if self.portfolio.inPortfolio(my_stock.getSymbol()):
            print("update " + my_stock.symbol )
        else:
            sql_insert = """INSERT INTO _bt_trades (symbol, amount, buy_date, buy_price) VALUES ('""" + my_stock.symbol + """',""" + str(my_amount) + """,'""" + my_date + """','""" + str(round(my_stock.getClose(),2)) + """')"""
            print(sql_insert)
            cursor.execute(sql_insert)
            self.adjustBalance(my_amount,-round(my_stock.getClose(),2))
            conn.commit()
        return 1

    def sell(self,my_stock,my_amount,my_date):
        DB_PATH = os.getenv("DB_PATH")
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        cursor = conn.cursor()
        if self.portfolio.inPortfolio(my_stock.symbol):
            if my_amount == self.portfolio.getStockAmount(my_stock.symbol):
                sql_update = """UPDATE _bt_trades SET sell_date = '""" + my_date + """', sell_price = """ + str(round(my_stock.getClose(),2)) + """ WHERE symbol = '""" + my_stock.symbol + """' AND sell_price IS NULL"""
                print(sql_update)
                print("sell all")
                self.adjustBalance(my_amount,sell_price)
                cursor.execute(sql_update)
                conn.commit()
            else:
                print("sell a bit")
                #sql_sell = """UPDATE _bt_trades setWHERE symbol = '""" + symbol + """' 
        else:
            print("nothing to sell")
            
    def adjustBalance(self,my_amount,buy_price):
        self.balance += my_amount * buy_price
        
    def getBalance(self):
        return self.balance
        
    