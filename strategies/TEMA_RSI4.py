
from base.stock import Stock
import numpy as np
import pandas as pd 

class TEMA_RSI4(Stock):
    def __init__(self, my_stock):
        self.stock = my_stock
        self.position = 0

    def define_position(self):
        final_position = pd.Series()
        loopcount = 0
        for index, row in self.stock.stockdata.iterrows():
            if loopcount == 0:
                prev1_row = row
            elif loopcount == 1:
                prev2_row = prev1_row
            else:
                # Enter a position
                if(((row['RSI_X_ABOVE_30']==1) or prev1_row['RSI_X_ABOVE_30']==1 or prev2_row['RSI_X_ABOVE_30']==1) and \
                   ((row['TEMA5_X_ABOVE_TEMA20']==1) or prev1_row['TEMA5_X_ABOVE_TEMA20']==1 or prev2_row['TEMA5_X_ABOVE_TEMA20']==1) and \
                   ((row['MACD_X_ABOVE_MACDSignal']==1) or prev1_row['MACD_X_ABOVE_MACDSignal']==1 or prev2_row['MACD_X_ABOVE_MACDSignal']==1) and \
                    self.position == 0):                
                #if ((row['TEMA5_X_ABOVE_TEMA20']==1 or row['RSI_X_ABOVE_30']==1 or row['MACD_X_ABOVE_MACDSignal']==1) 
                #    and row['TEMA20_ABOVE_SMA50'] and row['RSI_ABOVE_30'] and row['MACD_ABOVE_MACDSignal'] and self.position == 0):
                    if pd.notna(pd.Series([1]).any()):
                        #print(row['Date'] + " - Entering: (TEMA5_X_ABOVE_TEMA20=" + str(row['TEMA5_X_ABOVE_TEMA20']) + " or RSI_X_ABOVE_30=" + str(row['RSI_X_ABOVE_30']) + " or MACD_X_ABOVE_MACDSignal=" + str(row['MACD_X_ABOVE_MACDSignal']) + ") and TEMA20_ABOVE_SMA50=" + str(row['TEMA20_ABOVE_SMA50']) + " and RSI_ABOVE_50=" + str(row['RSI_ABOVE_50']) + " and MACD_ABOVE_MACDSignal=" + str(row['MACD_ABOVE_MACDSignal']) + ")")
                        final_position = pd.concat([final_position,pd.Series([1])], ignore_index=True)
                        self.position = 1

                # Exit a position
                if(((row['RSI_X_BELOW_70']==1) or prev1_row['RSI_X_BELOW_70']==1 or prev2_row['RSI_X_BELOW_70']==1) and \
                   ((row['TEMA5_X_BELOW_TEMA20']==1) or prev1_row['TEMA5_X_BELOW_TEMA20']==1 or prev2_row['TEMA5_X_BELOW_TEMA20']==1) and \
                   ((row['MACD_X_BELOW_MACDSignal']==1) or prev1_row['MACD_X_BELOW_MACDSignal']==1 or prev2_row['MACD_X_BELOW_MACDSignal']==1) and \
                    self.position == 1):           
                #elif ((row['TEMA5_X_BELOW_TEMA20']==1 or row['RSI_X_BELOW_70']==1 or row['MACD_X_BELOW_MACDSignal']==1 or row['TEMA20_BELOW_SMA50'] or row['RSI_BELOW_70'] or row['MACD_BELOW_MACDSignal']) and self.position == 1):
                    if pd.notna(pd.Series([0]).any()):
                        #print(row['Date'] + " - Exiting: (TEMA5_X_BELOW_TEMA20=" + str(row['TEMA5_X_BELOW_TEMA20']) + " or RSI_X_BELOW_70=" + str(row['RSI_X_BELOW_70']) + " or MACD_X_BELOW_MACDSignal=" + str(row['MACD_X_BELOW_MACDSignal']) + ") and TEMA20_BELOW_SMA50=" + str(row['TEMA20_BELOW_SMA50']) + " and RSI_BELOW_50=" + str(row['RSI_BELOW_50']) + " and MACD_BELOW_MACDSignal=" + str(row['MACD_BELOW_MACDSignal']) + ")")
                        final_position = pd.concat([final_position,pd.Series([0])], ignore_index=True)
                        self.position = 0
                # Keep a position
                else:
                    if pd.notna(pd.Series([self.position]).any()):
                        final_position = pd.concat([final_position,pd.Series([self.position])], ignore_index=True)
                
            loopcount = loopcount + 1
        return final_position