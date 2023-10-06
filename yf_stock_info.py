import yfinance as yf
import pandas as pd

def main():
    yf.pdr_override()
    pd.set_option('display.max_columns', None)
    tickers = ['AAPL']
    for my_ticker in tickers:
        my_stock = yf.Ticker(my_ticker)
        #my_stock_info_dict = my_stock.info
        #my_stock_info_pd = pd.DataFrame.from_dict(my_stock_info_dict,orient='index')
        #print(my_stock_info_pd)
        print(my_stock.get_incomestmt())

if __name__ == "__main__":
    main()

