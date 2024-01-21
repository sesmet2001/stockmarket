
from base.stock import Stock
import numpy as np
import pandas as pd 

class TEMA_RSI4(Stock):
    def __init__(self, my_stock):
        self.stock = my_stock
        self.position = 0

    def define_position(self):
        position_df = pd.DataFrame(columns=["TEMA_RSI4"])
        position_df.index.name = "Date"
        loopcount = 0
        debug = 0
        #print("in strat " + str(len(self.stock.stockdata)))
        for index, row in self.stock.stockdata.iterrows():
            if loopcount == 0:
                prev1_row = row
                position_df.loc[index, 'TEMA_RSI4'] = 0
            elif loopcount == 1:
                prev2_row = prev1_row
                position_df.loc[index, 'TEMA_RSI4'] = 0
            elif loopcount == 2:
                prev3_row = prev2_row
                position_df.loc[index, 'TEMA_RSI4'] = 0
            elif loopcount == 3:
                prev4_row = prev3_row
                position_df.loc[index, 'TEMA_RSI4'] = 0
            else:
                # Enter a position
                if((row['RSI_X_ABOVE_30']==1 or prev1_row['RSI_X_ABOVE_30']==1 or prev2_row['RSI_X_ABOVE_30']==1) and \
                   (row['TEMA5_X_ABOVE_TEMA20']==1 or prev1_row['TEMA5_X_ABOVE_TEMA20']==1 or prev2_row['TEMA5_X_ABOVE_TEMA20']==1) and \
                   (row['MACD_X_ABOVE_MACDSignal']==1 or prev1_row['MACD_X_ABOVE_MACDSignal']==1 or prev2_row['MACD_X_ABOVE_MACDSignal']==1) and \
                    self.position == 0):                
                #if ((row['TEMA5_X_ABOVE_TEMA20']==1 or row['RSI_X_ABOVE_30']==1 or row['MACD_X_ABOVE_MACDSignal']==1) 
                #    and row['TEMA20_ABOVE_SMA50'] and row['RSI_ABOVE_30'] and row['MACD_ABOVE_MACDSignal'] and self.position == 0):
                    if pd.notna(pd.Series([1]).any()):
                        #print(row['Date'] + " - Entering: (TEMA5_X_ABOVE_TEMA20=" + str(row['TEMA5_X_ABOVE_TEMA20']) + " or RSI_X_ABOVE_30=" + str(row['RSI_X_ABOVE_30']) + " or MACD_X_ABOVE_MACDSignal=" + str(row['MACD_X_ABOVE_MACDSignal']) + ") and TEMA20_ABOVE_SMA50=" + str(row['TEMA20_ABOVE_SMA50']) + " and RSI_ABOVE_50=" + str(row['RSI_ABOVE_50']) + " and MACD_ABOVE_MACDSignal=" + str(row['MACD_ABOVE_MACDSignal']) + ")")
                        position_df.loc[index, 'TEMA_RSI4'] = 1
                        self.position = 1
                    else:
                        print("enter o-oh")

                # Exit a position
                elif((row['RSI_X_BELOW_70']==1 or prev1_row['RSI_X_BELOW_70']==1 or prev2_row['RSI_X_BELOW_70']==1) and \
                   (row['TEMA5_X_BELOW_TEMA20']==1 or prev1_row['TEMA5_X_BELOW_TEMA20']==1 or prev2_row['TEMA5_X_BELOW_TEMA20']==1) and \
                   (row['MACD_X_BELOW_MACDSignal']==1 or prev1_row['MACD_X_BELOW_MACDSignal']==1 or prev2_row['MACD_X_BELOW_MACDSignal']==1) and \
                    self.position == 1):           
                #elif ((row['TEMA5_X_BELOW_TEMA20']==1 or row['RSI_X_BELOW_70']==1 or row['MACD_X_BELOW_MACDSignal']==1 or row['TEMA20_BELOW_SMA50'] or row['RSI_BELOW_70'] or row['MACD_BELOW_MACDSignal']) and self.position == 1):
                    if pd.notna(pd.Series([0]).any()):
                        #print(row['Date'] + " - Exiting: (TEMA5_X_BELOW_TEMA20=" + str(row['TEMA5_X_BELOW_TEMA20']) + " or RSI_X_BELOW_70=" + str(row['RSI_X_BELOW_70']) + " or MACD_X_BELOW_MACDSignal=" + str(row['MACD_X_BELOW_MACDSignal']) + ") and TEMA20_BELOW_SMA50=" + str(row['TEMA20_BELOW_SMA50']) + " and RSI_BELOW_50=" + str(row['RSI_BELOW_50']) + " and MACD_BELOW_MACDSignal=" + str(row['MACD_BELOW_MACDSignal']) + ")")
                        position_df.loc[index, 'TEMA_RSI4'] = 0
                        self.position = 0
                    else:
                        print("exit o-oh")
                # Keep a position
                else:
                    if pd.notna(pd.Series([self.position]).any()):
                        position_df.loc[index, 'TEMA_RSI4'] = self.position
                    else:
                        print("stay o-oh")
                prev4_row = prev3_row
                prev3_row = prev2_row
                prev2_row = prev1_row
                prev1_row = row 
            loopcount = loopcount + 1
        #print("end of strat loopcount " + str(loopcount))
        #print("end of strat " + str(len(final_position)))
        return position_df