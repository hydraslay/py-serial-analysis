# add following env var to solve error [Could not create cudnn handle: CUDNN_STATUS_INTERNAL_ERROR]
# export TF_FORCE_GPU_ALLOW_GROWTH=true

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
from joblib import dump, load

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

company = 'FB'

start = dt.datetime(2012, 1, 1)
end = dt.datetime(2020, 1, 1)

data = web.DataReader(company, 'yahoo', start, end)

# scaler = MinMaxScaler(feature_range=(0, 1))
scaler = load('MinMaxScaler.joblib')
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
# dump(scaler, 'MinMaxScaler.joblib')
pred_days = 10
x_train = []
y_train = []

for x in range(pred_days, len(scaled_data)):
    x_train.append(scaled_data[x - pred_days: x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)
model.save('model.mdl')
''' Test The Model Accuracy on Existing Data '''

test_start = dt.datetime(2020, 1, 1)
test_end = dt.datetime.now()

test_data = web.DataReader(company, 'yahoo', test_start, test_end)
actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']),axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - pred_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

x_test = []

for x in range(pred_days, len(model_inputs)):
    x_test.append(model_inputs[x - pred_days: x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

pred_prices = model.predict(x_test)
pred_prices = scaler.inverse_transform(pred_prices)

plt.plot(actual_prices, color='black', label=f'Actual {company} Price')
plt.plot(pred_prices, color='green', label=f'Prediction {company} Price')
plt.title(f'{company} Share Price')
plt.xlabel('Time')
plt.ylabel(f'{company} Share Price')
plt.legend()
plt.show()
