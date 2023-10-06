import yfinance as yf
import plotly.graph_objs as go

my_www_path = '/var/www/html'
my_periods = {'30d':'30 Days','1y':"Year",'5y':'5 Years'}

for my_period, my_period_name in my_periods.items():
    fig = go.Figure()
    bitcoin_data = yf.download('BTC-USD', period=my_period)

    fig.add_trace(go.Scatter(x=bitcoin_data.index, y=bitcoin_data['Close'], mode='lines', name='Bitcoin Close Price'))

    # Customize the layout
    fig.update_layout(
        title='Bitcoin Price the past ' + my_period_name,
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False
    )

    fig.write_image(my_www_path + '/images/bitcoin_price_plot-' + my_period + '.png', width=800, height=600)
