
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

my_ticker = 'NVDA'

today = date.today()
hundred_days_ago = today - timedelta(days=100)
four_years_ago_minus_hundred_days = today - timedelta(days=4 * 365.25) - hundred_days_ago

DB_PATH = os.getenv('DB_PATH')
conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
my_stock_train = Stock(conn_data,my_ticker,four_years_ago_minus_hundred_days,hundred_days_ago)
my_stock_test = Stock(conn_data,my_ticker,hundred_days_ago,today)

print(my_stock_train.stockdata)
print(my_stock_test.stockdata)

dataset_train = my_stock_train.stockdata
dataset_test = my_stock_test.stockdata
regressor = load_model("C:/Users/idefi/Documents/Scripts/stockmarket/regressor_model1.keras")
sc = MinMaxScaler(feature_range = (0, 1))
#training_set_scaled = sc.fit_transform(training_set)

real_stock_price = dataset_test.iloc[:, 1:2].values
print(dataset_test)

dataset_total = pd.concat((dataset_train['Open'],dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.fit_transform(inputs)

print(len(inputs))

X_test = []
for i in range(60, 129):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

plt.plot(real_stock_price, color = 'red', label = 'Real ' + my_ticker  + ' Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted ' + my_ticker  + ' Stock Price')
plt.xlabel('Time')
plt.ylabel(my_ticker + ' Stock Price')
plt.legend
plt.show()