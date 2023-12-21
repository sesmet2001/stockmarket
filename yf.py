import pandas as pd
import yfinance as yf
import timeit
import os
import sqlite3
from yahoo_fin import stock_info

def get_info(tickers):
    column_names = ['sector',
                        'fullTimeEmployees', 
                        'longBusinessSummary',
                        'website',
                        'industry',
                        'previousClose',
                        'regularMarketOpen',
                        'twoHundredDayAverage',
                        'regularMarketDayHigh',
                        'averageDailyVolume10Day',
                        'regularMarketPreviousClose',
                        'fiftyDayAverage',
                        'open',
                        'averageVolume10days',
                        'regularMarketDayLow',
                        'regularMarketVolume',
                        'marketCap',
                        'averageVolume',
                        'dayLow',
                        'ask',
                        'volume',
                        'fiftyTwoWeekHigh',
                        'forwardPE',
                        'fiftyTwoWeekLow',
                        'bid',
                        'dayHigh',
                        'shortName',
                        'longName',
                        'symbol',
                        'enterpriseToRevenue',
                        'profitMargins',
                        'enterpriseToEbitda',
                        '52WeekChange',
                        'morningStarRiskRating',
                        'forwardEps',
                        'bookValue',
                        'lastFiscalYearEnd',
                        'netIncomeToCommon',
                        'trailingEps',
                        'SandP52WeekChange',
                        'nextFiscalYearEnd',
                        'mostRecentQuarter',
                        'enterpriseValue',
                        'regularMarketPrice'] 
        
    info_df = pd.DataFrame(columns=column_names)
    for ticker in tickers:
        print(ticker)
        try:
            my_ticker = yf.Ticker(ticker)
            my_ticker_info = my_ticker.info
            my_ticker_info_filtered = { key:value for key, value in my_ticker_info.items() if key in column_names }
            my_ticker_info_filtered_df = pd.DataFrame(my_ticker_info_filtered,index=[0])
            info_df = info_df.append(my_ticker_info_filtered_df,ignore_index=True)
        except Exception as e:
            print(e)
            pass
    return info_df

def main():
    yf.pdr_override() 

    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
    cur = conn.cursor()
 
    #my_tickers = """SELECT Ticker FROM _yahoo_fin_tickers LIMIT 5"""
    #cur.execute(my_tickers)
    #tickers = cur.fetchall()
    #tickers = [x[0] for x in tickers]
    tickers = ['AAPL','GOOG']
    for ticker in tickers:
        my_financials = stock_info.get_financials(ticker)
        print(type(my_financials))
    #get_info(tickers).to_sql('_yf_info', conn, if_exists='replace')  

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()