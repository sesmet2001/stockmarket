from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class SMARevert(Indicator):
    def __init__(self,stock):
        self.type = "RSI"
        self.stock = stock
        
    def buy(self):
        self.stock.df.dropna(subset=['SMA50PercentChange'], inplace=True)
        if len(self.stock.df) > 5:
            if self.stock.df['SMA50PercentChange'].iloc[-4] < 0 and self.stock.df['SMA50PercentChange'].iloc[-3] < 0 and self.stock.df['SMA50PercentChange'].iloc[-2] > 0 and self.stock.df['SMA50PercentChange'].iloc[-1] > 0:
                print("BUY !!! " + self.stock.symbol + " df['RSI'].iloc[-2]:" + str(self.stock.df['RSI'].iloc[-2]) + " < 30 and df['RSI'].iloc[-1]:" + str(self.stock.df['RSI'].iloc[-1]) + " > 30")
                return 1
            else:
                return 0
        else:
            return 0

    def sell(self):
        self.stock.df.dropna(subset=['SMA50PercentChange'], inplace=True)
        if len(self.stock.df) > 5:
            if self.stock.df['SMA50PercentChange'].iloc[-4] > 0 and self.stock.df['SMA50PercentChange'].iloc[-3] > 0 and self.stock.df['SMA50PercentChange'].iloc[-2] < 0 and self.stock.df['SMA50PercentChange'].iloc[-1] < 0:
                print("SELL !!! " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0
