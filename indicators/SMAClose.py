from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class SMAClose(Indicator):
    def __init__(self,stock):
        self.type = "RSI"
        self.stock = stock
        self.margin = 1.5
        
    def buy(self):
        self.stock.df.dropna(subset=['SMA50'], inplace=True)
        if len(self.stock.df) > 70:
            if ((self.stock.df['SMA50'].iloc[-9] < self.stock.df['SMA50'].iloc[-7]) and \
            (self.stock.df['SMA50'].iloc[-7] < self.stock.df['SMA50'].iloc[-5]) and \
            (self.stock.df['SMA50'].iloc[-5] < self.stock.df['SMA50'].iloc[-3]) and \
            (self.stock.df['SMA50'].iloc[-3] < self.stock.df['SMA50'].iloc[-1]) and \
            (self.stock.df['Close'].iloc[-9] < self.stock.df['Close'].iloc[-7]) and \
            (self.stock.df['Close'].iloc[-7] < self.stock.df['Close'].iloc[-5]) and \
            (self.stock.df['Close'].iloc[-5] < self.stock.df['Close'].iloc[-3]) and \
            (self.stock.df['Close'].iloc[-3] < self.stock.df['Close'].iloc[-1])):
                return 1
            else:
                return 0
        else:
            return 0


    def sell(self):
        self.stock.df.dropna(subset=['SMA50'], inplace=True)
        if len(self.stock.df) > 70:
            if (self.stock.df['Close'].iloc[-9] - self.stock.df['SMA50'].iloc[-9] > 0) and \
                ((self.stock.df['Close'].iloc[-9] - self.stock.df['SMA50'].iloc[-9]) > (self.stock.df['Close'].iloc[-7] - self.stock.df['SMA50'].iloc[-7])) and \
                (self.stock.df['Close'].iloc[-7] - self.stock.df['SMA50'].iloc[-7] > 0) and \
                ((self.stock.df['Close'].iloc[-7] - self.stock.df['SMA50'].iloc[-7]) > (self.stock.df['Close'].iloc[-5] - self.stock.df['SMA50'].iloc[-5])) and \
                (self.stock.df['Close'].iloc[-3] - self.stock.df['SMA50'].iloc[-3] < 0) and \
                ((self.stock.df['Close'].iloc[-5] - self.stock.df['SMA50'].iloc[-5]) < (self.stock.df['Close'].iloc[-3] - self.stock.df['SMA50'].iloc[-3])) and \
                (self.stock.df['Close'].iloc[-1] - self.stock.df['SMA50'].iloc[-1] < 0) and \
                ((self.stock.df['Close'].iloc[-3] - self.stock.df['SMA50'].iloc[-3]) < (self.stock.df['Close'].iloc[-1] - self.stock.df['SMA50'].iloc[-1])):
                return 1
            else:
                return 0
        else:
            return 0
