import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from datetime import date, datetime, timedelta
import os
import sqlite3
from base.stock import Stock
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout






#X_predict = X_train[-1:]
#predicted_stock_prices = []
#for i in range(60, 60 + tradingdays_to_predict):    
#    predicted_stock_price = regressor.predict(X_predict)
#    print(predicted_stock_price)
#    X_predict = np.append(X_predict, predicted_stock_price)
#    X_predict = X_predict[-60:]
#    X_predict = np.reshape(X_predict, (1, X_predict.shape[0], 1))
#    print(sc.inverse_transform(predicted_stock_price))
#    print(type(sc.inverse_transform(predicted_stock_price)))
#    predicted_stock_prices.append(sc.inverse_transform(predicted_stock_price)[0])

#print(predicted_stock_prices)
#my_stock_to_plot = Stock(conn_data,my_ticker,four_years_before,prediction_start + timedelta(days=tradingdays_to_predict))
#real_stock_price = my_stock_to_plot.stockdata['Open'][-tradingdays_to_predict:]
#real_stock_price = real_stock_price.reset_index()
#print(real_stock_price)
