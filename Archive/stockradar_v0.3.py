from base.stock import Stock
import yfinance as yf
import sqlite3
import os
import pandas as pd
import numpy as np
from indicators.volume import Volume
from indicators.bbands import BBands
from indicators.upseries import UpSeries
from indicators.downseries import DownSeries
from indicators.minervini import Minervini
from indicators.RSI import RSI
from indicators.BB import BB
from indicators.SMACross import SMACross
from indicators.SMARevert import SMARevert
from indicators.SMACrossClose import SMACrossClose
from indicators.TEMACrossClose import TEMACrossClose
from indicators.SMAClose import SMAClose
import itertools
from datetime import date, datetime, timedelta
from collections import defaultdict

# def volume(my_stock):
#     signal = 0
#     my_stock.quotes['Volume_pctchange'] = my_stock.quotes['Volume'].pct_change()
#     if my_stock.quotes.iloc[-1,-1] > 25:
#         print(my_stock.quotes.iloc[-1,-1])
#         signal = 1
#     else:
#         signal = 0
#     return signal

# def close(my_stock):
#     signal = 0
#     my_stock.quotes['Close_pctchange'] = my_stock.quotes['Adj Close'].pct_change()
#     if my_stock.quotes.iloc[-1,-1] > 0.5:
#         print(my_stock.quotes.iloc[-1,-1])
#         signal = 1
#     else:
#         signal = 0
#     return signal

def main():
    DB_PATH = os.getenv("DB_PATH")

    conn = sqlite3.connect(DB_PATH + "/stockradar.db")
    cur = conn.cursor()
  
    scores = []
    upseriesdict = defaultdict(list)
    downseriesdict = defaultdict(list)
    volumedict = defaultdict(list)
    minervinidict = defaultdict(list)
    start_date = datetime.now() - timedelta(days=365)
    end_date = date.today()
    #end_date = "2021-10-07"

    returns_multiples = []
    ############ LOAD TICKERS ############
    sqlsymbols = """SELECT Ticker FROM _tickers_sp500"""
    # sqlsymbols = """SELECT Ticker FROM _portfolio 
    # UNION SELECT Ticker FROM _watchlist 
    # UNION SELECT Ticker FROM _tickers_dow
    # UNION SELECT Ticker FROM _tickers_sp500
    # UNION SELECT Ticker FROM _tickers_nasdaq"""
    #sqlsymbols = """SELECT Symbol FROM _symbols_euronext UNION SELECT Symbol FROM _symbols_nasdaq UNION SELECT Symbol FROM _symbols_sp500"""
    #sqltickers = """SELECT ticker FROM _portfolio"""

    tickers = cur.execute(sqlsymbols).fetchall()
    tickers = [x[0] for x in tickers]

    #index_df = yf.download("^IXIC", start_date, end_date)
    #index_df['Percent Change'] = index_df['AdjClose'].pct_change()
    #index_return = (index_df['Percent Change'] + 1).cumprod()[-1]

    signalsdf = pd.DataFrame(tickers)
    
    signalsdf.columns=['Ticker']
    signalsdf.set_index('Ticker')
    buy_RSI = []
    sell_RSI = []
    buy_BB = []
    sell_BB = []
    buy_SMACross = []
    sell_SMACross = []
    buy_SMACrossClose = []
    sell_SMACrossClose = []
    buy_TEMACrossClose = []
    sell_TEMACrossClose = []
    buy_SMARevert = []
    sell_SMARevert = []
    buy_SMAClose = []
    sell_SMAClose = []

    #sql_delete = "DELETE FROM _tickers_euronext WHERE Ticker = '"
    #tickers = ["NET"]
    for ticker in tickers:
        try:
            print(ticker)
            sql_query = pd.read_sql_query("""SELECT * from '""" + ticker + """' ORDER BY Date""",conn)
            df = pd.DataFrame(sql_query, columns=['Date','Ticker','AdjClose','Close','High','Low','Open','Volume','VolumePercentChange','ClosePercentChange','SMA50PercentChange','RSI','MACD','MACDSignal','MACDHist','SMA50','SMA150','SMA200','TEMA50','BB_low','BB_mid','BB_up'])
            my_stock = Stock(ticker, end_date)
            
            
            if type(my_stock.df['AdjClose'].iloc[0:1][0]) == np.float64:
                # upseries
                #upSeriesResult = UpSeries(my_stock).analyse()
                #upseriesdict[ticker].append(upSeriesResult[0])
                #upseriesdict[ticker].append(upSeriesResult[1])
    
                # downseries
                #downSeriesResult = DownSeries(my_stock).analyse()
                #downseriesdict[ticker].append(downSeriesResult[0])
                #downseriesdict[ticker].append(downSeriesResult[1])
    
                # volume up
                #volumeResult = Volume(my_stock).analyse()
                #volumedict[ticker].append(volumeResult)
    
                # BB crossover
                buy_BB.append(BB(my_stock).buy())
                sell_BB.append(BB(my_stock).sell())
                    
                # RSI crossover
                buy_RSI.append(RSI(my_stock).buy())
                sell_RSI.append(RSI(my_stock).sell())
                
                # SMA_crossover
                #buy_SMACross.append(SMACross(my_stock).buy())
                #sell_SMACross.append(SMACross(my_stock).sell()) 
    
                # SMA_crossover
                buy_SMACrossClose.append(SMACrossClose(my_stock).buy())
                sell_SMACrossClose.append(SMACrossClose(my_stock).sell()) 
                
                # TEMA_crossover
                buy_TEMACrossClose.append(TEMACrossClose(my_stock).buy())
                sell_TEMACrossClose.append(TEMACrossClose(my_stock).sell()) 
                
                # SMA_revert
                buy_SMARevert.append(SMARevert(my_stock).buy())
                sell_SMARevert.append(SMARevert(my_stock).sell())   
                
                # SMA_close
                buy_SMAClose.append(SMAClose(my_stock).buy())
                sell_SMAClose.append(SMAClose(my_stock).sell())  
    
                # Minervini
                #print(my_stock.df['Close Percent Change'].cumprod()[-1])
                #stock_return = (my_stock.df['Close Percent Change'] + 1).cumprod().iloc[-1]
                #returns_multiple = round((stock_return / index_return), 2)
                #returns_multiples.extend([returns_multiple])
            else:
                print(ticker)
                #sql_delete += ticker + "' OR Ticker = '"
        except Exception as ex:
            print(ex)
            buy_BB.append(0)
            sell_BB.append(0)
            buy_RSI.append(0)
            sell_RSI.append(0)
            buy_SMACrossClose.append(0)
            sell_SMACrossClose.append(0)
            buy_TEMACrossClose.append(0)
            sell_TEMACrossClose.append(0)
            buy_SMARevert.append(0)
            sell_SMARevert.append(0)
            buy_SMAClose.append(0)
            sell_SMAClose.append(0)
            pass

    #print(buy_BB)
    signalsdf["buy_BB"] = buy_BB
    signalsdf["sell_BB"] = sell_BB
    signalsdf["buy_RSI"] = buy_RSI
    signalsdf["sell_RSI"] = sell_RSI
    #signalsdf["buy_SMACross"] = buy_SMACross
    #signalsdf["sell_SMACross"] = sell_SMACross
    signalsdf["buy_SMACrossClose"] = buy_SMACrossClose
    signalsdf["sell_SMACrossClose"] = sell_SMACrossClose
    signalsdf["buy_TEMACrossClose"] = buy_TEMACrossClose
    signalsdf["sell_TEMACrossClose"] = sell_TEMACrossClose
    signalsdf["buy_SMAClose"] = buy_SMAClose
    signalsdf["sell_SMAClose"] = sell_SMAClose
    signalsdf["buy_SMARevert"] = buy_SMARevert
    signalsdf["sell_SMARevert"] = sell_SMARevert
    #signalsdf["Volume"] = sell_RSI
    signalsdf.to_sql('_signals', con=conn, if_exists='replace')
    #rs_df = pd.DataFrame(list(zip(tickers, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
    #rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
    #print(rs_df)
    #rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]
    #tickers_minervini = rs_df['Ticker']
    #rs_df = rs_df.set_index("Ticker")
    #for ticker_minervini in tickers_minervini:
        #print("********" + ticker_minervini)
        #sql_query = pd.read_sql_query("""SELECT * from '""" + ticker_minervini + """' ORDER BY Date""",conn)
        #df = pd.DataFrame(sql_query, columns=['Date','Ticker','Adj Close','Close','High','Low','Open','Volume','Volume Percent Change','Close Percent Change','SMA50','SMA150','SMA200','BB_low','BB_mid','BB_up'])
        #my_stock = Stock(ticker_minervini, df)  
        #minerviniResult = Minervini(my_stock).analyse()
        #print(ticker_minervini + ": " + str(minerviniResult))
        #if not minerviniResult:
            #rs_df.drop(ticker_minervini,axis=0,inplace=True)
            #print('drop' + ticker_minervini)
        #print(rs_df)

    # create and store dataframes in database
    #print(upseriesdict)
    #upseriesdf = pd.DataFrame.from_dict(upseriesdict,orient='index',columns=['UpsDays', 'UpsPct'])
    #upseriesdf.to_sql("_upseries", con=conn, if_exists='replace')

    #downseriesdf = pd.DataFrame.from_dict(downseriesdict,orient='index',columns=['DownsDays', 'DownsPct'])
    #downseriesdf.to_sql("_downseries", con=conn, if_exists='replace')

    #volumedf = pd.DataFrame.from_dict(volumedict,orient='index',columns=['Volume Pct Change'])
    #volumedf.to_sql("_volume", con=conn, if_exists='replace')

    #minervinidf = rs_df
    #minervinidf.to_sql("_minervini", con=conn, if_exists='replace')

    #RSIdf = pd.DataFrame.from_dict(RSIdict,orient='index',columns=['RSI buy', 'RSI sell'])
    #RSIdf.to_sql("_rsi-cross", con=conn, if_exists='replace')

    #my_stock.minervi()
    #scores.append([ticker,Volume(my_stock).analyse()])
    #print(postrains)

    #sort_dict = dict(reversed(sorted((value, key) for (key,value) in postrains.items())))
    #print(dict(itertools.islice(sort_dict.items(), 20)))
    #dfgains = pd.DataFrame.from_dict(gains,orient='index',columns=['Gains'])
    #dfgains = dfgains.sort_values(by=['Gains'], ascending="False").tail(50)
    #dfgains['Date'] = datetime.today().strftime('%Y-%m-%d')
    
    #dfgains_pct = pd.DataFrame.from_dict(gains_pct,orient='index',columns=['Gains Pct'])
    #dfgains_pct = dfgains_pct.sort_values(by=['Gains Pct'], ascending="False").tail(50)
    #dfgains_pct['Date'] = datetime.today().strftime('%Y-%m-%d')
    #dfgains_pct.to_sql("_gains_pct", con=conn, if_exists='append')

##    dflosses = pd.DataFrame.from_dict(losses,orient='index',columns=['Losses'])
##    dflosses = dflosses.sort_values(by=['Losses'], ascending="False").tail(50)
##    dflosses['Date'] = datetime.today().strftime('%Y-%m-%d')
##    dflosses.to_sql("_losses", con=conn, if_exists='append')
##
##    dflosses_pct = pd.DataFrame.from_dict(losses_pct,orient='index',columns=['Losses Pct'])
##    dflosses_pct = dflosses_pct.sort_values(by=['Losses Pct'], ascending="False").tail(50)
##    dflosses_pct['Date'] = datetime.today().strftime('%Y-%m-%d')
##    dflosses_pct.to_sql("_losses_pct", con=conn, if_exists='append')
        
    #dfscores = pd.DataFrame(scores, columns = ['ticker', 'volume_score'])
    #dfscores.sort_values(by=['volume_score'], inplace=True,ascending=False)
    #print(dfscores.head(50))
if __name__ == "__main__":
    main()
