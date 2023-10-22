from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class DownSeries(Indicator):

    def __init__(self,stock):
        self.type = "Down series"
        self.stock = stock

    def analyse(self):
        len = 0
        x = 1
        loss = 0
        try:
            while True:
                if self.stock.df['Close Percent Change'].iloc[-x] < 0:
                    len = len + 1
                    loss = loss + self.stock.df['Close Percent Change'].iloc[-x]
                    x = x + 1            
                else:
                    break
        except Exception as e:
            print(e)
        
        return [len, loss]