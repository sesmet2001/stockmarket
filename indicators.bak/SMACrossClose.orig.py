from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class SMACrossClose(Indicator):
    def __init__(self,stock):
        self.type = "RSI"
        self.stock = stock
        self.margin = 1.5
        
    def buy(self):
        self.stock.df.dropna(subset=['TEMA50'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['Close'].iloc[-3] < self.stock.df['TEMA50'].iloc[-3] and self.stock.df['Close'].iloc[-1] > self.stock.df['TEMA50'].iloc[-1]:
                #print("TEMA50 CROSS CLOSE BUY " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0

    def sell(self):
        self.stock.df.dropna(subset=['TEMA50'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['Close'].iloc[-2] > self.stock.df['TEMA50'].iloc[-2] and self.stock.df['Close'].iloc[-1] < self.stock.df['TEMA50'].iloc[-1]:
                #print("TEMA50 CROSS CLOSE SELL " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0
