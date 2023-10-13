from indicator import Indicator
import talib.abstract as ta
import pandas as pd
import math
import talib.abstract as ta
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
import sys
import numpy as np

class Minervini(Indicator):

    def __init__(self,stock):
        self.type = "Minervini"
        self.stock = stock

    def buy(self):
        signal = 0
        debug = 1

        try:
            currentClose = self.stock.df['Adj Close'].iloc[-1]
            moving_average_50 = self.stock.df['SMA50'].iloc[-1]
            moving_average_150 = self.stock.df['SMA150'].iloc[-1]
            moving_average_200 = self.stock.df['SMA200'].iloc[-1]
            low_of_52week = min(self.stock.df['Adj Close'].iloc[-260:])
            high_of_52week = max(self.stock.df['Adj Close'].iloc[-260:])

            if(moving_average_50 == None or moving_average_150 == None or moving_average_200 == None or low_of_52week == None or high_of_52week == None):
                return signal

            try:
                moving_average_200_20 = self.stock.df['SMA200'].iloc[-20]
            except Exception:
                moving_average_200_20 = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            if(currentClose > moving_average_150 > moving_average_200):
                if debug:
                    print("condition 1 is true")
                condition_1 = True
            else:
                condition_1 = False
                
            # Condition 2: 150 SMA and > 200 SMA
            if(moving_average_150 > moving_average_200):
                if debug:
                    print("condition 2 is true")
                condition_2 = True
            else:
                condition_2 = False
                
            # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
            if(moving_average_200 > moving_average_200_20):
                if debug:
                    print("condition 3 is true")
                condition_3 = True
            else:
                condition_3 = False
                
            # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            if(moving_average_50 > moving_average_150 > moving_average_200):
                if debug:
                    print("condition 4 is true")
                condition_4 = True
            else:
                condition_4 = False
                
            # Condition 5: Current Price > 50 SMA
            if(currentClose > moving_average_50):
                if debug:
                    print("condition 5 is true")
                condition_5 = True
            else:
                condition_5 = False
                
            # Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
            if(currentClose >= (1.3*low_of_52week)):
                if debug:
                    print("condition 6 is true")
                condition_6 = True
            else:
                condition_6 = False
                
            # Condition 7: Current Price is within 25% of 52 week high
            if(currentClose >= (.75*high_of_52week)):
                if debug:
                    print("condition 7 is true")
                condition_7 = True
            else:
                condition_7 = False
                
            if(condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7): 
                signal = 1
                #final.append(stock)
                #index.append(n)
                
                #dataframe = pd.DataFrame(list(zip(final, index)), columns =['Company', 'Index'])
                
                #dataframe.to_csv('stocks.csv')
                
                #exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating ,"50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)

        except Exception as e:
            print ("Error2" + str(e))
            #print("No data on "+ self.ticker)
        return signal 
    
    def sell(self):
        self.stock.data.dropna(subset=['SMA50'], inplace=True)
        self.stock.data.dropna(subset=['TEMA20'], inplace=True)
        if len(self.stock.data) > 60:
            if ((self.stock.data['SMA50'].iloc[-5] < self.stock.data['TEMA20'].iloc[-5]) and \
                (self.stock.data['SMA50'].iloc[-2] > self.stock.data['TEMA20'].iloc[-2])):
                #(np.gradient(self.stock.data['SMA150']<0))):
                #(self.stock.data['SMA50'].iloc[-10] > self.stock.data['SMA50'].iloc[-3] > self.stock.data['SMA50'].iloc[-1])):
                if self.debug:
                    print(self.stock.data['Date'].iloc[-1] + " - Indicator TEMA20CrossSMA50 Short - sell " + self.stock.symbol)
                    print("SMA50: " + str(self.stock.data['SMA50'].iloc[-5])  + "  < TEMA20: " + str(self.stock.data['TEMA20'].iloc[-5]))
                    print("SMA50: " + str(self.stock.data['SMA50'].iloc[-2])  + "  > TEMA20: " + str(self.stock.data['TEMA20'].iloc[-2]))
                return 1
            else:
                return 0
        else:
            return 0

    def plotgraph(self,imagepath,my_transaction):
        try:
            imagepath =  imagepath + self.stock.data['Date'].iloc[-1].split()[0] + "/" + my_transaction + "/" 
            if not os.path.isdir(imagepath):
                os.makedirs(imagepath)
            fig, ax = plt.subplots(nrows=2, ncols=1)
            #fig = plt.figure()
            #ax1 = fig.add_subplot(2,1,1)
            #fig, axs = plt.subplots(2)
            ax[0].title("TEMA20 cross SMA50 - " + self.stock.security + " (" + self.stock.symbol + ") " + self.stock.data['Date'].iloc[-1].split()[0])
            ax[0].plot(pd.to_datetime(self.stock.data['Date']).dt.date,self.stock.data['Close'], color = 'lightgrey', label = 'Close')
            ax[0].plot(pd.to_datetime(self.stock.data['Date']).dt.date,self.stock.data['SMA50'], color = 'red', label = 'SMA50')
            ax[0].plot(pd.to_datetime(self.stock.data['Date']).dt.date,self.stock.data['TEMA20'], color = 'cornflowerblue', label = 'TEMA20')
            ax[0].xticks(rotation=45)       
            ax[0].legend(loc="upper left")
            ax[0].gcf().autofmt_xdate()
            ax[1].plot(pd.to_datetime(self.stock.data['Date']).dt.date,self.stock.data['RSI'], color = 'lightgrey', label = 'Close')
            plt.savefig(imagepath + self.stock.symbol + ".png")
            #ax1.clf()
            #ax2.clf()
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            print(exception_traceback.tb_lineno)
            print(e)