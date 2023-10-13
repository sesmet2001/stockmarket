from base.asset import Asset
#import TA-lib.abstract as ta
import pandas as pd
import os
import sqlite3

class Stock(Asset):
    def __init__(self, symbol, my_date):
        DB_PATH = os.getenv("DB_PATH")
        conn = sqlite3.connect(DB_PATH + "/stockradar.db")
        sql_stock = pd.read_sql_query("SELECT * from '" + symbol + "' WHERE Date <= '" + str(my_date) + "'",conn)
        self.symbol = symbol
        self.df = pd.DataFrame(sql_stock)
        self.type = "stock"

    def dropna(self):
        self.df.dropna(subset=['Close'], inplace=True)
        
    def BBands(self):
        self.df['BB_up'], self.df['BB_mid'], self.df['BB_low'] = ta.BBANDS(self.df['Close'], timeperiod=20)
    
    def SMA(self,period):
        self.df["SMA" + str(period)] = ta.SMA(self.df['Close'],period)
        
    def TEMA(self,period):
        self.df["TEMA" + str(period)] = ta.TEMA(self.df['Close'],period)

    def RSI(self):
        self.df["RSI"] = ta.RSI(self.df['Close'],timeperiod=6)

    def MACD(self,MACD_FAST,MACD_SLOW,MACD_SIGNAL):
        self.df['MACD'], self.df['MACDSignal'], self.df['MACDHist'] = ta.MACD(self.df['Close'], fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)

    def Close_pct_change(self):
        self.df['ClosePercentChange'] = self.df['AdjClose'].pct_change()

    def Volume_pct_change(self):
        self.df['VolumePercentChange'] = self.df['Volume'].pct_change()

    def SMA50_pct_change(self):
        self.df['SMA50PercentChange'] = self.df['SMA50'].pct_change()

    def IBD_RS(self):
        current = self.df['AdjClose'][-1]
        c63 = self.df['AdjClose'][-63]
        c126 = self.df['AdjClose'][-126]
        c189 = self.df['AdjClose'][-189]
        c252 = self.df['AdjClose'][-252]
        return ((((current - c63) / c63) * .4) + (((current - c126) / c126) * .2) + (((current - c189) / c189) * .2) + (((current - c252) / c252) * .2)) * 100

    def Avg_mondays(self):
        return self.df[self.df.index.weekday==0]

    def LossTrain(self):
        len = 0
        x = 1
        loss = 0
        try:
            while True:
                if self.df['PercentChange'].iloc[-x] < 0:
                    len = len + 1
                    loss = loss + self.df['PercentChange'].iloc[-x]
                    x = x + 1                
                else:
                    break
        except:
            pass
        return len, loss

    def getAssetType(self):
        return Asset.getAssetType(self)

    def getSymbol(self):
        return self.symbol

    def getQuotes(self):
        return self.df
    
    def getClose(self):
        return self.df['Close'].iloc[-1]
    
    def getLastDate(self):
        return self.df['Date'].iloc[-1]

    #def getEMA(self, period, field='Close'):
    #    return self.ema = ta.EMA(self.quotes, timeperiod=period, price=field)
