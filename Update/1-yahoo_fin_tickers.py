import sqlite3
import yahoo_fin.stock_info as si
import pandas as pd
import sqlite3
import os

def main():
    try:
        # Define variables
        DB_PATH = os.getenv('DB_PATH')
        conn_info = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
        pd.set_option('display.max_columns', None)

        # Dow Jones tickers
        lst_dow_tickers = si.tickers_dow()
        pd_dow_tickers = pd.DataFrame({"Ticker": lst_dow_tickers})
        pd_dow_tickers.set_index(['Ticker'])

        # SP500 tickers
        lst_sp500_tickers = si.tickers_sp500()
        pd_sp500_tickers = pd.DataFrame({"Ticker": lst_sp500_tickers})
        pd_sp500_tickers.set_index(['Ticker'])

        # Nasdaq tickers
        lst_nasdaq_tickers = si.tickers_nasdaq()
        pd_nasdaq_tickers = pd.DataFrame({"Ticker": lst_nasdaq_tickers})
        pd_nasdaq_tickers.set_index(['Ticker'])

        # # Other tickers
        # lst_other_tickers = si.tickers_other()
        # pd_other_tickers = pd.DataFrame({"Ticker": lst_other_tickers})
        # pd_other_tickers.set_index(['Ticker'])

        # Concat and remove duplicates
        pd_all_tickers = pd.concat([pd_dow_tickers, pd_sp500_tickers, pd_nasdaq_tickers])
        pd_all_tickers = pd_all_tickers.drop_duplicates()

        # Mark tickers
        for index, row in pd_all_tickers.iterrows():
            for my_ticker in lst_dow_tickers:
                if my_ticker == row['Ticker']:
                    pd_all_tickers.loc[pd_all_tickers['Ticker'] == my_ticker, "Dow"] = 1
            for my_ticker in lst_sp500_tickers:
                if my_ticker == row['Ticker']:
                    pd_all_tickers.loc[pd_all_tickers['Ticker'] == my_ticker, "SP500"] = 1
            for my_ticker in lst_nasdaq_tickers:
                if my_ticker == row['Ticker']:
                    pd_all_tickers.loc[pd_all_tickers['Ticker'] == my_ticker, "Nasdaq"] = 1

        pd_all_tickers.to_sql('_yahoo_fin_tickers', con=conn_info, if_exists='replace')
        conn_info.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()