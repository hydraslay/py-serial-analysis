# add following env var to solve error [Could not create cudnn handle: CUDNN_STATUS_INTERNAL_ERROR]
# export TF_FORCE_GPU_ALLOW_GROWTH=true

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
import os
import tensorflow as tf
from joblib import dump, load

from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.utils import to_categorical

epochs = 100


def start_fit(x_train, y_train, x_add=[]):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_x_train = scaler.fit_transform(x_train)

    if len(x_add) == len(x_train):
        add_scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_x_add = add_scaler.fit_transform(x_add)
        scaled_x_train = np.concatenate((scaled_x_train, scaled_x_add), axis=1)

    x_train, y_train = np.array(scaled_x_train), np.array(y_train)

    # x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    # y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1], 1))
    # y_train = to_categorical(y_train)

    model = Sequential()

    model.add(Dense(units=64, input_shape=(x_train.shape[1],)))
    model.add(Dropout(0.5))
    model.add(Dense(units=64))
    model.add(Dropout(0.5))
    model.add(Dense(units=3, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    model.fit(x_train, y_train, epochs=epochs)
    model.save(os.path.join('tmp', 'model'))


def start_predict():
    model = tf.keras.models.load_model(os.path.join('tmp', 'model'))

    # test_start = dt.datetime(2020, 1, 1)
    # test_end = dt.datetime.now()
    #
    # test_data = web.DataReader(company, 'yahoo', test_start, test_end)
    # actual_prices = test_data['Close'].values
    #
    # total_dataset = pd.concat((data['Close'], test_data['Close']),axis=0)
    #
    # model_inputs = total_dataset[len(total_dataset) - len(test_data) - pred_days:].values
    # model_inputs = model_inputs.reshape(-1, 1)
    # model_inputs = scaler.transform(model_inputs)
    #
    # x_test = []
    #
    # for x in range(pred_days, len(model_inputs)):
    #     x_test.append(model_inputs[x - pred_days: x, 0])
    #
    # x_test = np.array(x_test)
    # x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    #
    # pred_prices = model.predict(x_test)
    # pred_prices = scaler.inverse_transform(pred_prices)