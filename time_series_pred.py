import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from os import listdir

from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf 
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.optimizers import Adam
from keras.models import load_model
from keras.callbacks import ModelCheckpoint

def string_to_float(money_str):
	return float(money_str.replace(",",""))

scaler = MinMaxScaler(feature_range=(0, 1))

file_name = 'nifty_it_historical_data.csv'

hist_data = pd.read_csv(file_name)
hist_data['Date'] = pd.to_datetime(hist_data.Date)
hist_data.index = hist_data['Date']
hist_data['Price'] = hist_data['Price'].apply(string_to_float)

sorted_hist_data = hist_data.sort_index(ascending=True, axis=0)
req_data = pd.DataFrame(index=range(0,len(hist_data)),columns=['Date', 'Close'])

for i in range(0,len(sorted_hist_data)):
	req_data['Date'][i] = sorted_hist_data['Date'][i]
	req_data['Close'][i] = sorted_hist_data['Price'][i]

req_data.index = req_data.Date
req_data.drop('Date', axis=1, inplace=True)

dataset = req_data.values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

train = scaled_data[0:3500,:]
valid = scaled_data[3500:,:]

x_train, y_train = [], []
for i in range(60,len(train)):
    x_train.append(scaled_data[i-60:i,0])
    y_train.append(scaled_data[i,0])
x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

inputs = req_data[len(req_data) - len(valid) - 60:].values
inputs = inputs.reshape(-1,1)
inputs  = scaler.transform(inputs)

X_test = []
for i in range(60,inputs.shape[0]):
    X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)

X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)

rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
print(rms)


# plt.figure(figsize=(16,8))
# plt.plot(hist_data['Price'], label='Close Price history')
# plt.show()