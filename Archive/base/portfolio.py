import talib.abstract as ta
import pandas as pd
from base.stock import Stock
import sqlite3
import os

class Portfolio():
   
    
    def __init__(self,my_balance):
        self.my_stocklist = []
        self.my_balance = my_balance
        DB_PATH = os.getenv("DB_PATH")
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        sql_portfolio = pd.read_sql_query("SELECT * from '_bt_trades' WHERE sell_date IS NULL",conn)
        self.df = pd.DataFrame(sql_portfolio)   

    def buy(self,my_stock,my_amount,my_date):
        DB_PATH = os.getenv("DB_PATH")
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        cursor = conn.cursor()
        if self.inPortfolio(my_stock.getSymbol()):
            print("Stock " + my_stock.symbol + " already in portfolio.")
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
        if self.inPortfolio(my_stock.symbol):
            if my_amount == self.getStockAmount(my_stock.symbol):
                sql_update = """UPDATE _bt_trades SET sell_date = '""" + my_date + """', sell_price = """ + str(round(my_stock.getClose(),2)) + """ WHERE symbol = '""" + my_stock.symbol + """' AND sell_price IS NULL"""
                print(sql_update)
                print("sell all")
                self.adjustBalance(my_amount,round(my_stock.getClose(),2))
                cursor.execute(sql_update)
                conn.commit()
            else:
                print("sell a bit")
                #sql_sell = """UPDATE _bt_trades setWHERE symbol = '""" + symbol + """' 
        else:
            print("nothing to sell")

    def getStocks(self):
        return self.df['symbol'].values

    def inPortfolio(self,symbol):
        DB_PATH = os.getenv("DB_PATH")
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        sql_portfolio = pd.read_sql_query("SELECT * from '_bt_trades' WHERE sell_date IS NULL",conn)
        self.df = pd.DataFrame(sql_portfolio)   
        if symbol in self.df['symbol'].values:
            return 1
        else:
            return 0
          
    def display(self):
        print(self.df.to_string())
        
    def getStockAmount(self,symbol):
        if self.inPortfolio(symbol):
            return self.df[self.df['symbol'] == symbol]['amount'].values[0]
        else:
            return 0

    def adjustBalance(self,my_amount,buy_price):
        self.my_balance += my_amount * buy_price

    def getBalance(self,my_date):
        DB_PATH = os.getenv("DB_PATH")
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        sql_portfolio = pd.read_sql_query("SELECT * from '_bt_trades' WHERE sell_date IS NULL",conn)
        self.df = pd.DataFrame(sql_portfolio)   
        for index, row in self.df.iterrows():    
            if row['sell_price'] is None:
                print("open trade")
                self.my_balance += row['amount'] * Stock(row['symbol'],my_date).getClose()
            else:
                print("closed")
                self.my_balance += row['amount'] * row['sell_price']
        return self.my_balance
    
    
  
