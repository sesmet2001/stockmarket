import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from datetime import date, datetime, timedelta
import os
import sqlite3
import sys
from keras.models import load_model
from pathlib import Path
from base.stock import Stock
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

def init_model():
    regressor = Sequential()
    regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (60, 2)))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units = 50))
    regressor.add(Dropout(0.2))
    regressor.add(Dense(units = 1))
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')
    return regressor

def main():
    DB_PATH = os.getenv('DB_PATH')
    my_tickers = ['NVDA']
    train_start_date = datetime(2016, 1, 1)
    train_end_date = datetime(2023, 12, 31)
    test_start_date = datetime(2024, 10, 2)
    test_end_date = datetime(2024, 10, 26)
    my_epochs = 10
    conn_data = sqlite3.connect(DB_PATH + "/database/stockradar-lite-rrndata.db")

    my_model = init_model()
    for my_ticker in my_tickers:
        # Data preprocessing
        my_stock = Stock(conn_data,my_ticker,train_start_date,train_end_date)
        dataset_train = my_stock.stockdata
        training_set = dataset_train.iloc[:, [1,5]].values
        print(training_set)
        sc = MinMaxScaler(feature_range = (0, 1))
        training_set_scaled = sc.fit_transform(training_set)
        print(training_set_scaled.shape)
        X_train = []
        y_train = []
        for i in range(60, dataset_train.shape[0]):
            X_train.append(training_set_scaled[i-60:i, 0:2])
            y_train.append(training_set_scaled[i, 0:2])
        X_train, y_train = np.array(X_train), np.array(y_train)
        print("X_train shape: " + str(X_train.shape))
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],2))
        print("X_train shape: " + str(X_train[:5]))
        print("X_train, y_train has been built with shape " + str(X_train.shape))

        # Start training
        print("Training model on " + my_ticker + " from " + str(train_start_date) + " until " + str(train_end_date))
        my_model.fit(X_train, y_train, epochs = my_epochs, batch_size = 32)
        my_model.save("C:/Users/idefi/Documents/Scripts/stockmarket/models/regressor_model2.keras")

    # Loading model
    regressor = load_model("C:/Users/idefi/Documents/Scripts/stockmarket/models/regressor_model2.keras")
    print("Model loaded: " + str(regressor.summary()))
    
    for my_ticker in my_tickers:
        my_stock_train = Stock(conn_data,my_ticker,train_start_date,train_end_date)
        dataset_train = my_stock_train.stockdata
        my_stock_test = Stock(conn_data,my_ticker,test_start_date,test_end_date)
        dataset_test = my_stock_test.stockdata
        # Testing
        print("Testing from " + str(test_start_date) + " until " + str(test_end_date))
        real_stock_price = dataset_test.iloc[:, [1,5]].values
        dataset_total = pd.concat((dataset_train,dataset_test), axis=0)
        print(dataset_total.head(5))
        inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
        print(inputs[:5])
        inputs = inputs.reshape(-1,2)
        print(inputs[:5])
        inputs = sc.transform(inputs)

        X_test = []
        for i in range(60, 60 + len(my_stock_test.stockdata)):
            X_test.append(inputs[i-60:i, 0:2])
        X_test = np.array(X_test)
        print(X_test[:5])
        # Reshape to dimension ('batch size', 'timesteps', 'number of predictors')
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 2))
        print(X_test[:5])

        print("X_test.shape = " + str(X_test.shape[0]) + " - " + str(X_test.shape[1]))
        predicted_stock_price = regressor.predict(X_test)
        print(predicted_stock_price.size)
        predicted_stock_price = sc.inverse_transform(predicted_stock_price,)

        plt.plot(real_stock_price, color = 'red', label = 'Real ' + my_ticker  + ' Stock Price')
        plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted ' + my_ticker  + ' Stock Price')
        plt.xlabel('Time')
        plt.ylabel(my_ticker + ' Stock Price')
        plt.legend
        plt.show()

if __name__ == "__main__":
    main()