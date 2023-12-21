from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class RSI(Indicator):
    def __init__(self,stock):
        self.type = "RSI"
        self.stock = stock
        
    def buy(self):
        self.stock.df.dropna(subset=['RSI'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['RSI'].iloc[-2] < 30 and self.stock.df['RSI'].iloc[-1] > 30:
                #print("RSI BUY " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0

    def sell(self):
        self.stock.df.dropna(subset=['RSI'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['RSI'].iloc[-2] > 70 and self.stock.df['RSI'].iloc[-1] < 70:
                #print("RSI SELL " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0
