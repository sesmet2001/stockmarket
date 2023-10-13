# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:23:53 2021

@author: sefsmet
"""

import pandas as pd
import sqlite3
import os
from indicators.SMACrossClose import SMACrossClose
import datetime

class Strategy():
    def buy(self,my_stock):
        if SMACrossClose(my_stock).buy():
            #self.portfolio.buy(my_stock,200,my_stock.getLastDate())
            print("Buying "  + my_stock.symbol + " on CrossClose")
            return 1
        else:
            return 0

    def sell(self,my_stock):
        if SMACrossClose(my_stock).sell():
            #self.portfolio.sell(my_stock,200,my_stock.getLastDate())
            print("Selling "  + my_stock.symbol + " on CrossClose")
            return 1
        else:
            return 0
    