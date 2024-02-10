# Part 1 - Data Preprocessing

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from datetime import date, datetime, timedelta
import os
import sqlite3
import sys
from pathlib import Path
from base.stock import Stock

my_ticker = 'NVDA'

today = date.today()
hundred_days_ago = today - timedelta(days=100)
four_years_ago_minus_hundred_days = today - timedelta(days=4 * 365.25) - hundred_days_ago
print("Training from " + str(four_years_ago_minus_hundred_days) + " until " + str(hundred_days_ago))

DB_PATH = os.getenv('DB_PATH')
conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
my_stock = Stock(conn_data,my_ticker,four_years_ago_minus_hundred_days,hundred_days_ago)

dataset_train = my_stock.stockdata
training_set = dataset_train.iloc[:, 1:2].values

sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)
#print(training_set_scaled)

X_train = []
y_train = []
for i in range(60, dataset_train.shape[0]):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Part 2 - Building the RNN
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

regressor = Sequential()
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

regressor.save("C:/Users/idefi/Documents/Scripts/stockmarket/models/regressor_model1.keras")