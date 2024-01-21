
from base.stock import Stock
import numpy as np
import pandas as pd 
import sys

class TEMA_RSI(Stock):
    def __init__(self, my_stock):
        self.stock = my_stock
        self.position = 0

    #if pd.notna(pd.Series([0]).any()):
        
    def define_position(self):
        position_df = pd.DataFrame(columns=["TEMA_RSI"])
        position_df.index.name = "Date"
        try:
            for index, row in self.stock.stockdata.iterrows():
                if row['TEMA5_X_ABOVE_TEMA20']==1 and row['TEMA20_ABOVE_SMA50'] and self.position == 0:
                    position_df.loc[index, 'TEMA_RSI'] = 1
                    self.position = 1
                elif row['TEMA5_X_BELOW_TEMA20']==1 and self.position == 1:
                    position_df.loc[index, 'TEMA_RSI'] = 0
                    self.position = 0
                else:
                    position_df.loc[index, 'TEMA_RSI'] = self.position
        except Exception as e:
            # Get the exception information including the line number
            exc_type, exc_obj, exc_tb = sys.exc_info()
                
            # Extract the line number
            line_number = exc_tb.tb_lineno
                
            # Print the exception message along with the line number
            print(f"Exception occurred in apply-strategy on line {line_number}: {e}")
        return position_df