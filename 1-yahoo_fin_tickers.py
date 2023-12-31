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

        # Portfolio tickers
        lst_portfolio_tickers = ["NVDA","VUSA.AS","AMZN","AMD","ARM","CRM","ASML","ZIM","ALNOV.PA","HCP"]
        pd_portfolio_tickers = pd.DataFrame({"Ticker": lst_portfolio_tickers})
        pd_portfolio_tickers.set_index(['Ticker'])

        # Precious metals
        lst_precious_metals_tickers = ["GC=F","SI=F","PA=F","PL=F"]
        pd_precious_metals_tickers = pd.DataFrame({"Ticker": lst_precious_metals_tickers})
        pd_precious_metals_tickers.set_index(['Ticker'])

        # Oil
        lst_oil_tickers = ["CL=F"]
        pd_oil_tickers = pd.DataFrame({"Ticker": lst_oil_tickers})
        pd_oil_tickers.set_index(['Ticker'])

        # Crypto
        lst_crypto_tickers = ["BTC-USD","ETH-USD","BNB-USD","XRP-USD","SOL-USD","ADA-USD","DOGE-USD","LINK-USD","DOT-USD","SHIB-USD"]
        pd_crypto_tickers = pd.DataFrame({"Ticker": lst_crypto_tickers})
        pd_crypto_tickers.set_index(['Ticker'])

        # # Other tickers
        # lst_other_tickers = si.tickers_other()
        # pd_other_tickers = pd.DataFrame({"Ticker": lst_other_tickers})
        # pd_other_tickers.set_index(['Ticker'])

        # Concat and remove duplicates
        pd_all_tickers = pd.concat([pd_dow_tickers, pd_sp500_tickers, pd_nasdaq_tickers, pd_portfolio_tickers, pd_precious_metals_tickers, pd_oil_tickers, pd_crypto_tickers])
        pd_all_tickers = pd_all_tickers.drop_duplicates()

        print(pd_all_tickers)

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
            for my_ticker in lst_portfolio_tickers:
                if my_ticker == row['Ticker']:
                    pd_all_tickers.loc[pd_all_tickers['Ticker'] == my_ticker, "Portfolio"] = 1
            for my_ticker in lst_precious_metals_tickers:
                if my_ticker == row['Ticker']:
                    pd_all_tickers.loc[pd_all_tickers['Ticker'] == my_ticker, "PreciousMetals"] = 1
            for my_ticker in lst_oil_tickers:
                if my_ticker == row['Ticker']:
                    pd_all_tickers.loc[pd_all_tickers['Ticker'] == my_ticker, "Oil"] = 1
            for my_ticker in lst_crypto_tickers:
                if my_ticker == row['Ticker']:
                    pd_all_tickers.loc[pd_all_tickers['Ticker'] == my_ticker, "Crypto"] = 1

        pd_all_tickers.to_sql('_yahoo_fin_tickers', con=conn_info, if_exists='replace')
        conn_info.close()
        print("all done")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()