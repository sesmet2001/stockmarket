from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class SMACross(Indicator):
    def __init__(self,stock):
        self.type = "RSI"
        self.stock = stock
        
    def buy(self):
        self.stock.df.dropna(subset=['SMA50'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['SMA50'].iloc[-10] < self.stock.df['SMA150'].iloc[-10] and self.stock.df['SMA50'].iloc[-1] > self.stock.df['SMA150'].iloc[-1]:
                #print("BUY !!! " + self.stock.symbol + " df['RSI'].iloc[-2]:" + str(self.stock.df['RSI'].iloc[-2]) + " < 30 and df['RSI'].iloc[-1]:" + str(self.stock.df['RSI'].iloc[-1]) + " > 30")
                #print("BUY - SMA50 Cross up SMA150: " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0

    def sell(self):
        self.stock.df.dropna(subset=['SMA50'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['SMA50'].iloc[-10] > self.stock.df['SMA150'].iloc[-10] and self.stock.df['SMA50'].iloc[-1] < self.stock.df['SMA150'].iloc[-1]:
                #print("SELL - SMA50 Cross down SMA150: " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0
