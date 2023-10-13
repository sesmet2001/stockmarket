# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 15:04:23 2021

@author: sefsmet
"""

import sqlite3
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import seaborn as sns
from datetime import datetime, timedelta
import os

def reformat_large_tick_values(tick_val,pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000000:
        val = round(tick_val/1000000000, 1)
        new_tick_format = '{:}B'.format(val)
    elif tick_val >= 1000000:
        val = round(tick_val/1000000, 1)
        new_tick_format = '{:}M'.format(val)
    elif tick_val >= 1000:
        val = round(tick_val/1000, 1)
        new_tick_format = '{:}K'.format(val)
    elif tick_val < 1000:
        new_tick_format = round(tick_val, 1)
    else:
        new_tick_format = tick_val
        
    return new_tick_format

conn = sqlite3.connect("/var/www/destef_be/stockradar.db")
cur = conn.cursor()

sql_symbols = """SELECT DISTINCT Symbol FROM _yf_financials"""
cur.execute(sql_symbols)
symbols = cur.fetchall()
symbols = [x[0] for x in symbols]
#symbols = ['ADI','AAPL','AMZN']
df_netIncomeScores = pd.DataFrame(columns=['NetIncomePctChange'])
for symbol in symbols:
    sql_netIncome = """SELECT `Net Income` FROM _yf_financials WHERE Symbol = '""" + symbol + """' ORDER BY Date"""
    df_netIncome = pd.read_sql(sql_netIncome,conn)
    df_netIncome['NetIncomePctChange'] = df_netIncome['Net Income'].pct_change()
    new_row = {'Symbol':symbol, 'Net Income': df_netIncome.iloc[-1][0], 'NetIncomePctChange': df_netIncome.iloc[-1][1] }
    df_netIncomeScores = df_netIncomeScores.append(new_row, ignore_index=True)
#revenueScoresdf.set_index(['Symbol'], append=True, inplace=True)
df_netIncomeScores.to_sql('_yf_financials_netincome_scores', conn, if_exists='replace')
    

sqlscores = """SELECT * FROM _yf_financials_netincome_scores WHERE `Net Income` > 1000000 ORDER BY NetIncomePctChange DESC"""
cur.execute(sqlscores)
scores = cur.fetchall()
#for score in scores:
    #print(score)


sqlshortlist = """SELECT Symbol FROM _yf_financials_netincome_scores WHERE `Net Income` > 1000000 ORDER BY NetIncomePctChange DESC LIMIT 100"""
cur.execute(sqlshortlist)
shortlist = cur.fetchall()

dir_wamp = "/var/www/destef_be"
dir_netincome = dir_wamp + "/netincome" + "/" + datetime.today().strftime('%Y-%m-%d')

print("")
for symbol in shortlist:
    sql_query = pd.read_sql_query("""SELECT * from '""" + symbol[0] + """' ORDER BY Date""",conn)
    df = pd.DataFrame(sql_query, columns=['Date','Ticker','Adj Close','Close','High','Low','Open','Volume','Percent Change','SMA50','SMA150','SMA200','TEMA20','TEMA50','BB_low','BB_mid','BB_up'])#.tail(50)
    print(symbol[0])
    print(df.iloc[-1])
    #df.set_index('Date',inplace=True)
    plt.title(symbol[0])
    plt.plot(pd.to_datetime(df['Date']).dt.date,df['Close'], color = 'cornflowerblue', label = 'Close')
    #plt.plot(pd.to_datetime(df['Date']).dt.date,df['Low'], color = 'orange', label = 'Low')
    #plt.plot(pd.to_datetime(df['Date']).dt.date,df['High'], color = 'green', label = 'High')
    plt.plot(pd.to_datetime(df['Date']).dt.date,df['BB_low'], color = 'red', label = 'BB_low')
    plt.plot(pd.to_datetime(df['Date']).dt.date,df['BB_mid'], color = 'purple', label = 'BB_mid')
    plt.plot(pd.to_datetime(df['Date']).dt.date,df['BB_up'], color = 'brown', label = 'BB_up')
    plt.xticks(rotation=45)       
    plt.legend(loc="upper left")
    plt.gcf().autofmt_xdate()
    if not os.path.isdir(dir_netincome):
        os.makedirs(dir_netincome)
    plt.savefig(dir_netincome + "/" + symbol[0] + "-BB.png")
    plt.clf()

    plt.title(symbol[0])
    plt.plot(pd.to_datetime(df['Date']).dt.date,df['Close'], color = 'cornflowerblue', label = 'Close')
    plt.plot(pd.to_datetime(df['Date']).dt.date,df['TEMA20'], color = 'orange', label = 'TEMA20')
    plt.plot(pd.to_datetime(df['Date']).dt.date,df['TEMA50'], color = 'green', label = 'TEMA50')
    plt.xticks(rotation=45)       
    plt.legend(loc="upper left")
    plt.savefig(dir_netincome + "/" + symbol[0] + "-SMA.png")
    plt.clf()



    # sql_info = """SELECT * FROM _yf_info WHERE Symbol = '""" + symbol[0] + """'"""
    # df_info = pd.read_sql(sql_info,conn)
    # fig, (ax1, ax2) = plt.subplots(1,2) 
    # fig.set_figwidth(16)
    # print("Yahoo finance: https://finance.yahoo.com/quote/" + symbol[0])
    # #print(df_info)
    # print("Net income: x" + str(round(symbol[1],2)) + " compared to last year")
    # print("Employees: " + str(df_info['fullTimeEmployees'][0]))
    # print("Website: " + str(df_info['website'][0]))
    # #print("Business:" + str(df_info['longBusinessSummary'][0]))
    # sql_netIncome = """SELECT Symbol,Date,`Net Income` FROM _yf_financials WHERE Symbol = '""" + symbol[0] + """' ORDER BY Date"""
    # df_netIncome = pd.read_sql(sql_netIncome,conn)
    # ax1.set_title(symbol[0])
    # ax1.yaxis.set_major_formatter(reformat_large_tick_values);
    # ax1.plot(pd.to_datetime(df_netIncome['Date']).dt.date,df_netIncome['Net Income'], color = 'cornflowerblue', label = 'Net Income')
    # ax1.legend(loc="upper left")
    # ax1.tick_params(labelrotation=45)  
    # #plt.show()

    # sql_totalRevenue = """SELECT Symbol,Date,`Total Revenue` FROM _yf_financials WHERE Symbol = '""" + symbol[0] + """' ORDER BY Date"""
    # df_totalRevenue = pd.read_sql(sql_totalRevenue,conn)
    # ax2.set_title(symbol[0])
    # ax2.yaxis.set_major_formatter(reformat_large_tick_values);
    # ax2.plot(pd.to_datetime(df_totalRevenue['Date']).dt.date,df_totalRevenue['Total Revenue'], color = 'cornflowerblue', label = 'Total Revenue')
    # ax2.legend(loc="upper left")
    # ax2.tick_params(labelrotation=45) 
    # plt.show()
    # print("")