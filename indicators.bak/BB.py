from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class BB(Indicator):
    def __init__(self,stock):
        self.type = "RSI"
        self.stock = stock
        
    def buy(self):
        self.stock.df.dropna(subset=['BB_up'], inplace=True)
        self.stock.df.dropna(subset=['BB_mid'], inplace=True)
        self.stock.df.dropna(subset=['BB_low'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['AdjClose'].iloc[-2] < self.stock.df['BB_low'].iloc[-2] and self.stock.df['AdjClose'].iloc[-1] > self.stock.df['BB_low'].iloc[-1]:
                #if self.stock.symbol == "AAPL":
                #print("BUY !!! " + self.stock.symbol + "  -   AdjClose[-2]:" + str(self.stock.df['AdjClose'].iloc[-2]) + " < BB Low[-2]:" + str(self.stock.df['BB_low'].iloc[-2]) + " and AdjClose[-1]:" + str(self.stock.df['AdjClose'].iloc[-1]) + " > BB_low[-1]:" + str(self.stock.df['BB_low'].iloc[-1]))
                #print("BB BUY " + self.stock.symbol)
                return 1
            else:
                #if self.stock.symbol == "AAPL":
                #print(self.stock.symbol + "  -  AdjClose[-2]:" + str(self.stock.df['AdjClose'].iloc[-2]) + " <  BB Low[-2]:" + str(self.stock.df['BB_low'].iloc[-2]) + " and AdjClose[-1]:" + str(self.stock.df['AdjClose'].iloc[-1]) + " > BB_low[-1]:" + str(self.stock.df['BB_low'].iloc[-1]))
                return 0
        else:
            return 0

    def sell(self):
        self.stock.df.dropna(subset=['BB_up'], inplace=True)
        self.stock.df.dropna(subset=['BB_mid'], inplace=True)
        self.stock.df.dropna(subset=['BB_low'], inplace=True)
        if len(self.stock.df) > 1:
            if self.stock.df['AdjClose'].iloc[-2] > self.stock.df['BB_up'].iloc[-2] and self.stock.df['AdjClose'].iloc[-1] < self.stock.df['BB_up'].iloc[-1]:
                #print("BB SELL " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0
