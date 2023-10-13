from indicator import Indicator
import talib as ta
from talib import MA_Type
import pandas as pd
import math
import matplotlib.pyplot as plt


class BBands(Indicator):
    def __init__(self,stock):
        self.type = "bbands"
        self.stock = stock

    def calculate(self):
        self.stock.df.dropna(subset=['Close'], inplace=True)
        self.stock.df['BB_up'], self.stock.df['BB_mid'], self.stock.df['BB_low'] = ta.BBANDS(self.stock.df['Close'], timeperiod=20)
        print(df)
        
    def analyse(self):
        self.stock.df.dropna(subset=['Close'], inplace=True)
        self.stock.df['BB_up'], self.stock.df['BB_mid'], self.stock.df['BB_low'] = ta.BBANDS(self.stock.df['Close'], timeperiod=20)
        #upper, middle, lower = talib.BBANDS(self.stock.getQuotes()['Close'], matype=MA_Type.T3)
        #print(upper)
        #return float(self.stock.getQuotes().iloc[-1,-1])
