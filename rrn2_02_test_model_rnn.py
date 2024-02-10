
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

def my_train(train_start_date,train_end_date,X_train,y_train): 
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
    regressor.save("C:/Users/idefi/Documents/Scripts/stockmarket/models/regressor_model2.keras")


# Defining variables
my_ticker = 'NVDA'
tradingdays_to_test = 30
tradingdays_to_predict = 30
DB_PATH = os.getenv('DB_PATH')
conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-rrndata.db")
start_date = datetime(2016, 1, 1)
end_date = datetime.now().strftime('%Y-%m-%d')
train_start_date = start_date
train_end_date = datetime(2023, 12, 31)
test_start_date = datetime(2024, 1, 1)
test_end_date = datetime(2024, 1, 26)


# Part 1 - Data Preprocessing
my_stock_train = Stock(conn_data,my_ticker,train_start_date,train_end_date)
dataset_train = my_stock_train.stockdata
training_set = dataset_train.iloc[:, 1:2].values
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)
X_train = []
y_train = []
print(dataset_train.shape[0])
for i in range(60, dataset_train.shape[0]):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)
# Reshape to dimension ('batch size', 'timesteps', 'number of predictors')
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


# Part 2 - Training
print("Training from " + str(train_start_date) + " until " + str(train_end_date))
#my_train(train_start_date,train_end_date,X_train,y_train)


# Part 3 - Testing
print("Testing from " + str(test_start_date) + " until " + str(test_end_date))
regressor = load_model("C:/Users/idefi/Documents/Scripts/stockmarket/models/regressor_model2.keras")
print(regressor.summary())

my_stock_test = Stock(conn_data,my_ticker,test_start_date,test_end_date)
dataset_test = my_stock_test.stockdata
real_stock_price = dataset_test.iloc[:, 1:2].values

dataset_total = pd.concat((dataset_train['Open'],dataset_test['Open']), axis=0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)

X_test = []
for i in range(60, 60 + len(my_stock_test.stockdata)):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
# Reshape to dimension ('batch size', 'timesteps', 'number of predictors')
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

print("X_test.shape = " + str(X_test.shape[0]) + " - " + str(X_test.shape[1]))
predicted_stock_price = regressor.predict(X_test)
print(predicted_stock_price.size)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)


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

plt.plot(real_stock_price, color = 'red', label = 'Real ' + my_ticker  + ' Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted ' + my_ticker  + ' Stock Price')
plt.xlabel('Time')
plt.ylabel(my_ticker + ' Stock Price')
plt.legend
plt.show()