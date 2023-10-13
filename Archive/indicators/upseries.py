from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math

class UpSeries(Indicator):

    def __init__(self,stock):
        self.type = "Up series"
        self.stock = stock

    def analyse(self):
        len = 0
        x = 1
        #gain = []
        gain = 0
        try:
            while True:
                if self.stock.df['Close Percent Change'].iloc[-x] > 0:
                    len = len + 1
                    #gain = gain.append(self.stock.df['Percent Change'].iloc[-x])
                    gain = gain + self.stock.df['Close Percent Change'].iloc[-x]
                    x = x + 1            
                else:
                    break
        except Exception as e:
            print(e)
        
        return [len, gain]
