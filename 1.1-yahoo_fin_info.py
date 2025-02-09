import pandas as pd
import yfinance as yf
import timeit
import os
import sqlite3
import time

def main():
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite.db")
    cur = conn.cursor()
    counter = 0
    print("starting")

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
 
    tickers_sql = """SELECT Ticker FROM _yahoo_fin_tickers"""
    cur.execute(tickers_sql)
    my_tickers = cur.fetchall()
    my_tickers = [x[0] for x in my_tickers]
    for my_ticker in my_tickers:
        print(str(counter) + ": " + my_ticker)
        try:
            my_ticker_obj = yf.Ticker(my_ticker)
            my_ticker_info = my_ticker_obj.info
            my_ticker_info_filtered = { key:value for key, value in my_ticker_info.items() if key in column_names }
            my_ticker_info_filtered_df = pd.DataFrame(my_ticker_info_filtered,index=[0])
            my_ticker_info_filtered_df['Ticker'] = my_ticker
            info_df = pd.concat([info_df,my_ticker_info_filtered_df],ignore_index=True)
        except Exception as e:
            print(e)
            pass
        counter = counter + 1
        if counter % 100 == 0:
            print("Going to sleep 10 sec.")
            time.sleep(10)
    print(info_df)
    return info_df.to_sql('_yahoo_fin_info', conn, if_exists='replace')  

    # # revenue info
    # my_tickers = """SELECT Symbol FROM _yf_financials_revenue_scores WHERE `Total Revenue` > 1000000 ORDER BY RevenuePctChange DESC LIMIT 100"""
    # cur.execute(my_tickers)
    # tickers = cur.fetchall()
    # tickers = [x[0] for x in tickers]
    # get_info(tickers).to_sql('_yf_info', conn, if_exists='append')  

    # # watchlist info
    # my_tickers = """select Ticker from _watchlist"""
    # cur.execute(my_tickers)
    # tickers = cur.fetchall()
    # tickers = [x[0] for x in tickers]
    # get_info(tickers).to_sql('_yf_info', conn, if_exists='append')  
    
    # # portfolio info
    # my_tickers = """select Ticker from _portfolio"""
    # cur.execute(my_tickers)
    # tickers = cur.fetchall()
    # tickers = [x[0] for x in tickers]
    # get_info(tickers).to_sql('_yf_info', conn, if_exists='append')    

    # # buy_radar info
    # my_tickers = """select Ticker from _signals WHERE buy_SMACrossClose=1"""
    # cur.execute(my_tickers)
    # tickers = cur.fetchall()
    # tickers = [x[0] for x in tickers]
    # get_info(tickers).to_sql('_yf_info', conn, if_exists='append')
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()