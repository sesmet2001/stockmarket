import talib.abstract as ta
import pandas as pd
import math
import traceback
import sys

class Cross():
    def __init__(self,my_stock,my_column1,my_column2):
        self.my_stock = my_stock
        self.my_column1 = my_column1
        self.my_column2 = my_column2
        
    def detect(self):
        try:
            # Create a boolean series indicating where column1 < column2
            crossing_series = self.my_stock.stockdata[self.my_column1] < self.my_stock.stockdata[self.my_column2]

            # Determine where the crossing happens
            crossing_points = (crossing_series != crossing_series.shift()) & ~crossing_series.isna()

            # Assign direction indicators based on the crossing direction
            print(crossing_series)
            print(crossing_points)
            my_return = [ '-' if cp and crossing_series[idx] else ('+' if cp else ('<' if crossing_series[idx] else '>')) for idx, cp in enumerate(crossing_points) ]

            return my_return
        
        except Exception as e:
            # Get the exception information including the line number
            exc_type, exc_obj, exc_tb = sys.exc_info()
            
            # Extract the line number
            line_number = exc_tb.tb_lineno
            
            # Print the exception message along with the line number
            print(f"Exception occurred in cross on line {line_number}: {e}")