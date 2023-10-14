import yfinance as yf
import plotly.graph_objs as go
import os
import sqlite3

DB_PATH = os.getenv("DB_PATH")
WWW_PATH = os.getenv("DB_PATH")
my_periods = {"30d":"30 Days","1y":"Year","5y":"5 Years"}

conn = sqlite3.connect(DB_PATH + "/database/stockradar-lite-info.db")
cur = conn.cursor()

my_ticker_types = ["PreciousMetals","Crypto"]

my_tickers_query = """SELECT Ticker FROM _yahoo_fin_tickers WHERE """
for my_ticker_type in my_ticker_types:
    my_tickers_query += my_ticker_type + " == 1 OR """

my_tickers_query = my_tickers_query[:-3]

cur.execute(my_tickers_query)
my_tickers = cur.fetchall()
my_tickers = [x[0] for x in my_tickers]

for my_period, my_period_name in my_periods.items():
    fig = go.Figure()
    for my_ticker in my_tickers:
        print(my_period + "-" + my_ticker)
        ticker_data = yf.download(my_ticker, period=my_period)
        fig.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data["Close"], mode="lines", name=my_ticker))

        # Customize the layout
        fig.update_layout(
            title="Price the past " + my_period_name,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False
        )

        fig.write_image(WWW_PATH + "/images/" + my_ticker + "-" + my_period + ".png", width=800, height=600)
