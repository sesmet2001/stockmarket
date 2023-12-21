from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class TEMACrossClose(Indicator):
    def __init__(self,stock):
        self.type = "RSI"
        self.stock = stock
        self.margin = 1.5
        
    def buy(self):
        self.stock.df.dropna(subset=['TEMA50'], inplace=True)
        if len(self.stock.df) > 70:
            # if (self.stock.df['TEMA50'].iloc[-9] - self.stock.df['Close'].iloc[-9] > 0) and \
            #     ((self.stock.df['TEMA50'].iloc[-9] - self.stock.df['Close'].iloc[-9]) > (self.stock.df['TEMA50'].iloc[-7] - self.stock.df['Close'].iloc[-7])) and \
            #     (self.stock.df['TEMA50'].iloc[-1] - self.stock.df['Close'].iloc[-1] < 0) and \
            #     ((self.stock.df['TEMA50'].iloc[-3] - self.stock.df['Close'].iloc[-3]) < (self.stock.df['TEMA50'].iloc[-1] - self.stock.df['Close'].iloc[-1])):
            print(str(self.stock.df['TEMA50'].iloc[-4]) + " " + str(self.stock.df['Close'].iloc[-4]))
            print(str(self.stock.df['TEMA50'].iloc[-1]) + " " + str(self.stock.df['Close'].iloc[-1]))
            if (self.stock.df['TEMA50'].iloc[-4] > self.stock.df['Close'].iloc[-4]) and \
                (self.stock.df['TEMA50'].iloc[-1] < self.stock.df['Close'].iloc[-1]):
                print("BUY " + self.stock.symbol)
                return 1
            else:
                return 0
        else:
            return 0


    def sell(self):
        self.stock.df.dropna(subset=['TEMA50'], inplace=True)
        if len(self.stock.df) > 70:
            if (self.stock.df['Close'].iloc[-9] - self.stock.df['TEMA50'].iloc[-9] > 0) and \
                ((self.stock.df['Close'].iloc[-9] - self.stock.df['TEMA50'].iloc[-9]) > (self.stock.df['Close'].iloc[-7] - self.stock.df['TEMA50'].iloc[-7])) and \
                (self.stock.df['Close'].iloc[-1] - self.stock.df['TEMA50'].iloc[-1] < 0) and \
                ((self.stock.df['Close'].iloc[-3] - self.stock.df['TEMA50'].iloc[-3]) < (self.stock.df['Close'].iloc[-1] - self.stock.df['TEMA50'].iloc[-1])):
                return 1
            else:
                return 0
        else:
            return 0
