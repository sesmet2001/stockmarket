
from base.stock import Stock
import numpy as np
import pandas as pd 

class TEMA_RSI2(Stock):
    def __init__(self, my_stock):
        self.stock = my_stock
        self.position = 0

    def define_position(self):
        final_position = pd.Series()
        for index, row in self.stock.stockdata.iterrows():
            if row['TEMA5_X_ABOVE_TEMA20']==1 and self.position == 0:
                if pd.notna(pd.Series([1]).any()):
                    final_position = pd.concat([final_position,pd.Series([1])], ignore_index=True)
                    self.position = 1
            elif row['TEMA5_X_BELOW_TEMA20']==1 and self.position == 1:
                if pd.notna(pd.Series([0]).any()):
                    final_position = pd.concat([final_position,pd.Series([0])], ignore_index=True)
                    self.position = 0
            else:
                if pd.notna(pd.Series([self.position]).any()):
                    final_position = pd.concat([final_position,pd.Series([self.position])], ignore_index=True)
        return final_position