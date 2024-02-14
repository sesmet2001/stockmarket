
from base.stock import Stock
import numpy as np
import pandas as pd 
import sys

class Strat2(Stock):
    def __init__(self, my_stock):
        self.stock = my_stock
        self.position = 0
        self.weight_rsi = 1
        self.weight_macd = 1
        self.weight_sma50 = 1

    #if pd.notna(pd.Series([0]).any()):
        
    def define_position(self):

        self.stock.stockdata['STRAT2_BUY'] = \
            self.weight_sma50 * self.stock.stockdata['CLOSE_X_ABOVE_SMA50'] + \
            self.weight_macd * self.stock.stockdata['MACD_X_ABOVE_MACDSignal'] + \
            self.weight_rsi * self.stock.stockdata['RSI_X_ABOVE_30']
        self.stock.stockdata['STRAT2_SELL'] = \
            self.weight_sma50 * self.stock.stockdata['CLOSE_X_BELOW_SMA50'] + \
            self.weight_macd * self.stock.stockdata['MACD_X_BELOW_MACDSignal'] + \
            self.weight_rsi * self.stock.stockdata['RSI_X_BELOW_70']
        self.stock.stockdata['STRAT2_BUY-SELL'] = self.stock.stockdata['STRAT1_BUY'] - self.stock.stockdata['STRAT1_SELL']
        
        position_df = pd.DataFrame(columns=["Strat2"])

        position_df.index.name = "Date"
        try:
            for index, row in self.stock.stockdata.iterrows():
                if row['STRAT2_BUY-SELL'] > 2 and self.position == 0:
                    position_df.loc[index, 'Strat2'] = 1
                    self.position = 1
                elif row['STRAT2_BUY-SELL'] < -2 and self.position == 1:
                    position_df.loc[index, 'Strat2'] = 0
                    self.position = 0
                else:
                    position_df.loc[index, 'Strat2'] = self.position
        except Exception as e:
            # Get the exception information including the line number
            exc_type, exc_obj, exc_tb = sys.exc_info()
                
            # Extract the line number
            line_number = exc_tb.tb_lineno
                
            # Print the exception message along with the line number
            print(f"Exception occurred in apply-strategy on line {line_number}: {e}")
        return position_df