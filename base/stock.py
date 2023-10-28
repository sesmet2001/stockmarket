from base.asset import Asset
import talib.abstract as ta
import pandas as pd
import os
import sqlite3
import numpy as np
import itertools
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import plotly.io as pio 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Stock(Asset):
    def __init__(self, my_conn, my_ticker, my_enddate):
        self.type = "stock"
        self.ticker = my_ticker
        self.stockdata = pd.read_sql_query("SELECT * from '" + my_ticker + "' WHERE Date <= '" + str(my_enddate) + "'",my_conn)

    def dropna(self):
        self.stockdata.dropna(subset=['Close'], inplace=True)
        
    def BBands(self):
        self.stockdata['BB_up'], self.stockdata['BB_mid'], self.stockdata['BB_low'] = ta.BBANDS(self.stockdata['Close'], timeperiod=20)
    
    def SMA(self,period):
        self.stockdata["SMA" + str(period)] = ta.SMA(self.stockdata['Close'],period)
        
    def TEMA(self,period):
        self.stockdata["TEMA" + str(period)] = ta.TEMA(self.stockdata['Close'],period)

    def RSI(self):
        self.stockdata["RSI"] = ta.RSI(self.stockdata['Close'],timeperiod=6)

    def MACD(self,MACD_FAST,MACD_SLOW,MACD_SIGNAL):
        self.stockdata['MACD'], self.stockdata['MACDSignal'], self.stockdata['MACDHist'] = ta.MACD(self.stockdata['Close'], fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)

    def Close_pct_change(self):
        self.stockdata['ClosePercentChange'] = self.stockdata['AdjClose'].pct_change()

    def Volume_pct_change(self):
        self.stockdata['VolumePercentChange'] = self.stockdata['Volume'].pct_change()

    def SMA50_pct_change(self):
        self.stockdata['SMA50PercentChange'] = self.stockdata['SMA50'].pct_change()

    def IBD_RS(self):
        current = self.stockdata['AdjClose'][-1]
        c63 = self.stockdata['AdjClose'][-63]
        c126 = self.stockdata['AdjClose'][-126]
        c189 = self.stockdata['AdjClose'][-189]
        c252 = self.stockdata['AdjClose'][-252]
        return ((((current - c63) / c63) * .4) + (((current - c126) / c126) * .2) + (((current - c189) / c189) * .2) + (((current - c252) / c252) * .2)) * 100

    def Avg_mondays(self):
        return self.stockdata[self.stockdata.index.weekday==0]

    def LossTrain(self):
        len = 0
        x = 1
        loss = 0
        try:
            while True:
                if self.stockdata['PercentChange'].iloc[-x] < 0:
                    len = len + 1
                    loss = loss + self.stockdata['PercentChange'].iloc[-x]
                    x = x + 1                
                else:
                    break
        except:
            pass
        return len, loss

    def getAssetType(self):
        return Asset.getAssetType(self)

    def getTicker(self):
        return self.ticker

    def getQuotes(self):
        return self.df
    
    def getClose(self):
        return self.stockdata['Close'].iloc[-1]
    
    def getLastDate(self):
        return self.stockdata['Date'].iloc[-1]
    
    def plotbasegraph(self,my_imagepath,my_plotrange):
        try:
            self.plotdata = self.stockdata.tail(my_plotrange).copy()
            self.plotdata['Date2'] = self.plotdata['Date']
            self.plotdata.set_index('Date',inplace=True)
            fig = make_subplots(rows=2,cols=1,vertical_spacing = 0.10,row_heights=[0.7, 0.3],subplot_titles=(self.ticker + " Price ($)", "RSI"))
            fig.update_layout(width=1200, height=800, title_x=0.5)
            fig.update_layout(xaxis_rangeslider_visible=False)
            fig.add_trace(
                go.Candlestick(x=self.plotdata.index,open=self.plotdata['Open'],high=self.plotdata['High'],low=self.plotdata['Low'],close=self.plotdata['Close'],showlegend=False),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['SMA50'],mode='lines',name='SMA50'),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['TEMA5'],mode='lines',name='TEMA5'),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['TEMA20'],mode='lines',name='TEMA20'),
                row=1, col=1
            )
            #fig.add_trace(
            #    go.Bar(x=self.stockdata.index,y=self.stockdata['Volume'],name='Volume',showlegend=False,marker={"color": "rgba(128,128,128,0.5)"}),
            #    row=2, col=1
            #)
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['RSI'],mode='lines',name='RSI',showlegend=False,marker={"color": "rgba(128,128,128,0.5)"}),
                row=2, col=1
            )
            fig.add_shape(type='line',x0=self.plotdata.index.min(),y0=70,x1=self.plotdata.index.max(),y1=70,line=dict(color='Red'),row=2, col=1)
            fig.add_shape(type='line',x0=self.plotdata.index.min(),y0=30,x1=self.plotdata.index.max(),y1=30,line=dict(color='Green'),row=2, col=1)
            my_buy_signals = self.plotdata[self.plotdata['TEMA5_TEMA20_crossover'] == "bullish crossover"]
            my_sell_signals = self.plotdata[self.plotdata['TEMA5_TEMA20_crossover'] == "bearish crossover"]
            for i,row in my_buy_signals.iterrows():
                fig.add_vline(x=row.Date2, line_width=2, opacity=0.2, line_dash="dash", line_color="green")
            for i,row in my_sell_signals.iterrows():
                fig.add_vline(x=row.Date2, line_width=2, opacity=0.2, line_dash="dash", line_color="red")

            pio.write_image(fig, my_imagepath + self.ticker + ".png") 

        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            print(exception_traceback.tb_lineno)
            print(e)
