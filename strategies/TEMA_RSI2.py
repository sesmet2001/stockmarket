
from base.stock import Stock
import numpy as np
import pandas as pd 

class TEMA_RSI2(Stock):
    def __init__(self, my_stock):
        self.stock = my_stock
        self.position = 0

    def define_position(self):
        position_df = pd.DataFrame(columns=["TEMA_RSI2"])
        position_df.index.name = "Date"
        for index, row in self.stock.stockdata.iterrows():
            if row['TEMA5_X_ABOVE_TEMA20']==1 and self.position == 0:
                if pd.notna(pd.Series([1]).any()):
                    position_df.loc[index, 'TEMA_RSI2'] = 1
                    self.position = 1
            elif row['TEMA5_X_BELOW_TEMA20']==1 and self.position == 1:
                if pd.notna(pd.Series([0]).any()):
                    position_df.loc[index, 'TEMA_RSI2'] = 0
                    self.position = 0
            else:
                if pd.notna(pd.Series([self.position]).any()):
                    position_df.loc[index, 'TEMA_RSI2'] = self.position
        return position_df