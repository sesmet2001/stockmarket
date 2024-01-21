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
    def __init__(self, my_conn, my_ticker, my_startdate, my_enddate):
        self.type = "stock"
        self.ticker = my_ticker
        self.stockdata = pd.read_sql_query("SELECT * from '" + my_ticker + "' WHERE Date >= '" + str(my_startdate) + "' AND Date < '" + str(my_enddate) + "'",my_conn)
        self.stockdata.set_index("Date",inplace=True)
        #print(self.stockdata.head(10))

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

    def calculate_returns(self,my_startcapital):
        try: 
            #self.stockdata['DailyReturns'].dropna()
            #self.stockdata['Position'].dropna()
            print(self.stockdata['ClosePercentChange'])
            print(self.stockdata['Position'])
            #my_return = self.stockdata.loc['ClosePercentChange'].dot(self.stockdata.loc['Position'])
            #return my_return
            return my_startcapital
        except Exception as e:
            print(e)

    def plotbasegraph(self,my_imagepath,my_plotrange,my_strategies,my_colors):
        try:
            self.plotdata = self.stockdata.tail(my_plotrange).copy()
            #self.plotdata['Date2'] = self.plotdata['Date']
            #self.plotdata.set_index('Date',inplace=True)
            #if self.plotdata['CumulativeReturn'].iloc[-1]:
            #    fig = make_subplots(rows=6,cols=1,vertical_spacing = 0.05,row_heights=[0.50, 0.10, 0.10, 0.10, 0.10, 0.10],subplot_titles=(self.ticker + "\n Price ($)\n(" + datetime.today().strftime('%d/%m/%Y') + ")", "RSI", "MACD", "Volume", "Position", "Return: " + str(round(self.plotdata['CumulativeReturn'].iloc[-1]))))
            #else:
            #    fig = make_subplots(rows=6,cols=1,vertical_spacing = 0.05,row_heights=[0.50, 0.10, 0.10, 0.10, 0.10, 0.10],subplot_titles=(self.ticker + "\n Price ($)\n(" + datetime.today().strftime('%d/%m/%Y') + ")", "RSI", "MACD", "Volume", "Position", "Return"))
            fig = make_subplots(rows=6,cols=1,vertical_spacing = 0.05,row_heights=[0.50, 0.10, 0.10, 0.10, 0.10, 0.10],subplot_titles=(self.ticker + "\n Price ($)\n(" + datetime.today().strftime('%d/%m/%Y') + ")", "RSI", "MACD", "Volume", "Position", "Return"))
            
            fig.update_layout(width=1200, height=1600, title_x=0.5)
            fig.update_layout(xaxis_rangeslider_visible=False)
            
            # Row 1 Open Close
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
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['BB_up'],mode='lines',name='BB upper',line_color='grey',opacity=0.2),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['BB_mid'],mode='lines',name='BB middle',line_color='grey',opacity=0.1),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['BB_low'],mode='lines',name='BB lower',line_color='grey',opacity=0.2),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['SL_Price'],mode='markers',name='Stop Loss',line_color='red',opacity=1),
                row=1, col=1
            )
            #fig.add_trace(
            #    go.Bar(x=self.stockdata.index,y=self.stockdata['Volume'],name='Volume',showlegend=False,marker={"color": "rgba(128,128,128,0.5)"}),
            #    row=2, col=1
            #)

            # Row 2 RSI
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['RSI'],mode='lines',name='RSI',showlegend=False,marker={"color": "rgba(128,128,128,0.5)"}),
                row=2, col=1
            )
            fig.add_shape(type='line',x0=self.plotdata.index.min(),y0=70,x1=self.plotdata.index.max(),y1=70,line=dict(color='Red'),row=2, col=1)
            fig.add_shape(type='line',x0=self.plotdata.index.min(),y0=30,x1=self.plotdata.index.max(),y1=30,line=dict(color='Green'),row=2, col=1)

            # Row 3 MACD
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['MACD'],mode='lines',name='MACD'),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=self.plotdata.index,y=self.plotdata['MACDSignal'],mode='lines',name='MACD Signal'),
                row=3, col=1
            )
            fig.add_trace(
                go.Bar(x = self.plotdata.index, y = self.plotdata['MACDHist'],name='MACD Histogram',marker={"color": "rgba(128,128,128,0.5)"}),
                row=3, col=1
            )

            # Row 4 Volume
            fig.add_trace(
                go.Bar(x = self.plotdata.index, y = self.plotdata['Volume'],name='Volume',marker={"color": "rgba(128,128,128,0.5)"}),
                row=4, col=1
            )

            # Row 5 Position
            my_strategies = ["TEMA_RSI4"]
            colornbr = 0
            for my_strategy in my_strategies:
                fig.add_trace(
                    go.Scatter(x=self.plotdata.index,y=self.plotdata[my_strategy],mode='lines',marker_color=my_colors[colornbr],name=my_strategy),
                    row=5, col=1
                )
                colornbr = colornbr + 1

            # Row 6 Return
            colornbr = 0
            my_strategies = ["TEMA_RSI4"]
            for my_strategy in my_strategies:                
                fig.add_trace(
                    go.Scatter(x=self.plotdata.index,y=self.plotdata[my_strategy + "_total_return"],mode='lines',marker_color=my_colors[colornbr],name=my_strategy),
                    row=6, col=1
                )
                colornbr = colornbr + 1
            
            #f = pd.DataFrame()
            #df["Color"] = np.where(self.plotdata['DailyReturn']<0, 'red', 'green')
            #fig.add_trace(
            #    go.Bar(x=self.plotdata.index,y=self.plotdata['DailyReturn'],name='Return'),
            #    row=5, col=1
            #)
            #fig.update_traces(marker_color=df["Color"])

            # Add signals
            TEMA5_X_ABOVE_TEMA20 = self.plotdata[self.plotdata["TEMA5_X_ABOVE_TEMA20"] == 1]
            TEMA5_X_BELOW_TEMA20 = self.plotdata[self.plotdata["TEMA5_X_BELOW_TEMA20"] == 1]
            #for i,row in TEMA5_X_ABOVE_TEMA20.iterrows():
            #    fig.add_vline(x=row.Date2, line_width=2, opacity=0.3, line_dash="dash", line_color="green")
            #for i,row in TEMA5_X_BELOW_TEMA20.iterrows():
            #    fig.add_vline(x=row.Date2, line_width=2, opacity=0.3, line_dash="dash", line_color="red")

            pio.write_image(fig, file=my_imagepath + self.ticker + ".png", format="png", engine="kaleido") 
            return 1
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            print("plot error " + str(exception_traceback.tb_lineno))
            print(e)
