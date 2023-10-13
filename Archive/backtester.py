# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 18:45:02 2021

@author: sefsmet
"""

import os
import sqlite3
import pandas as pd
from base.portfolio import Portfolio
from base.trader import Trader
from base.strategy import Strategy
import datetime
from base.stock import Stock


# load portfolio
def main():
    start_date = datetime.date(2021, 5, 1)
    end_date = datetime.date(2022, 3, 3)
    my_balance = 50000

    
    DB_PATH = os.getenv("DB_PATH")
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH + "/stockradar.db")
    cursor = conn.cursor()
    sql_dates = """SELECT Date FROM 'AAPL' WHERE Date > '""" + str(start_date) + """' AND Date < '""" + str(end_date) + """'"""
    my_dates = cursor.execute(sql_dates).fetchall()

    my_portfolio = Portfolio(my_balance)
    
    print("START BALANCE: " + str(my_portfolio.getBalance(start_date)))
        
    for my_date in my_dates:
        print(my_date)
        # Load portfolio

        #print(my_portfolio.getStocks())
        #my_portfolio.display()        

        
        # create trader object 

         # launch buy strategy
        #for my_stock in my_portfolio.getStocks():
        for my_stock in ['FFIV','AAPL','NFLX','GOOG']:
            Strategy(my_portfolio).buy(Stock(my_stock,my_date[0]))    
        
        # launch sell strategy
        #for my_stock in my_portfolio.getStocks():
        for my_stock in ['FFIV','AAPL','NFLX','GOOG']:
            Strategy(my_portfolio).sell(Stock(my_stock,my_date[0]))

        
    print("END BALANCE: " + str(my_portfolio.getBalance(end_date)))

    
    
 
    # test buy 
    #my_trader.buy('AMD',10,'16/10/2021')
    
    # test sell
    #my_trader.sell('AMD',10,'16/10/2021')

        
    # # buy radar
        
    # # check balance (balance class)
        
    # # update portfolio
        
    # # show portfolio transactions
        
    # # show portfolio balance
    #print(round(my_portfolio.getBalance(),0))

if __name__ == "__main__":
    main()