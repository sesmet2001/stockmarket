from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math
import numpy as np

class Volume(Indicator):
    def __init__(self,stock):
        self.type = "volume"
        self.stock = stock
        
    def analyse(self):
        if type(self.stock.df['Volume Percent Change'].iloc[-1]) == np.float64:
            if self.stock.df['Volume'].iloc[-1] > 1000000 and self.stock.df['Volume'].iloc[-2] > 100000:
                return self.stock.df['Volume Percent Change'].iloc[-1]
            else:
                return 0
        else:
            return 0
