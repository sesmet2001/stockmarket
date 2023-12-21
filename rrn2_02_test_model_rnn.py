
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
four_years_ago = today - timedelta(days=4 * 365.25)

DB_PATH = os.getenv('DB_PATH')
conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-data.db")
my_stock_train = Stock(conn_data,my_ticker,four_years_ago,today)
#my_stock_test = ?



dataset_train = my_stock_train.stockdata
#dataset_test = my_stock_test.stockdata
regressor = load_model("C:/Users/idefi/Documents/Scripts/stockmarket/regressor_model2.keras")
sc = MinMaxScaler(feature_range = (0, 1))
#training_set_scaled = sc.fit_transform(training_set)

#real_stock_price = dataset_test.iloc[:, 1:2].values
#print(dataset_test)

dataset_total = dataset_train['Open']
inputs = dataset_total[:].values
inputs = inputs.reshape(-1,1)
inputs = sc.fit_transform(inputs)

print(len(inputs))
print(inputs)

X_test = []
X_test = inputs[-60:, 0]
for i in range(60, 62):    
    print(X_test)
    
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (1, X_test.shape[0], 1))

    predicted_stock_price = regressor.predict(X_test)
    print(predicted_stock_price)
    X_test = np.append(X_test, predicted_stock_price)
    X_test = X_test[-60:, 0]
    #predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    #print(predicted_stock_price)

#plt.plot(real_stock_price, color = 'red', label = 'Real ' + my_ticker  + ' Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted ' + my_ticker  + ' Stock Price')
plt.xlabel('Time')
plt.ylabel(my_ticker + ' Stock Price')
plt.legend
plt.show()