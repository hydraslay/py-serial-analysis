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
from tensorflow import keras

epochs = 1000


def start_fit(x_train, y_train_nc, x_add=[]):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_x_train = scaler.fit_transform(x_train)

    if len(x_add) == len(x_train):
        add_scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_x_add = add_scaler.fit_transform(x_add)
        scaled_x_train = np.concatenate((scaled_x_train, scaled_x_add), axis=1)

    x_train, y_train_nc = np.array(scaled_x_train), np.array(y_train_nc)
    # equalize count of each label
    lbl_cnt = []
    for lbl in range(np.max(y_train_nc) + 1):
        lbl_cnt.append((y_train_nc == lbl).sum())
    lbl_cnt = np.array(lbl_cnt)
    lbl_cnt = lbl_cnt - np.min(lbl_cnt)
    del_row = []
    for r in range(len(x_train)):
        val = y_train_nc[r][0]
        if lbl_cnt[val] > 0:
            del_row.append(r)
            lbl_cnt[val] = lbl_cnt[val] - 1
    x_train = np.delete(x_train, del_row, axis=0)
    y_train_nc = np.delete(y_train_nc, del_row, axis=0)
    lbl_cnt_after = []
    for lbl in range(np.max(y_train_nc) + 1):
        lbl_cnt_after.append((y_train_nc == lbl).sum())

    # x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    # y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1], 1))
    y_train = to_categorical(y_train_nc)

    model = Sequential()

    model.add(Dense(units=256, input_shape=(x_train.shape[1],)))
    model.add(Dropout(0.2))
    model.add(Dense(units=128))
    model.add(Dropout(0.2))
    model.add(Dense(units=64))
    model.add(Dropout(0.2))
    model.add(Dense(units=3, activation='softmax'))

    opt = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()
    model.fit(x_train, y_train, epochs=epochs, batch_size=x_train.shape[0])
    model.save(os.path.join('tmp', 'model'))

    pred_results = model.predict(x_train)
    y_pred = np.argmax(pred_results, axis=1)
    test_score = (y_train_nc == np.reshape(y_pred, (y_pred.shape[0], 1))).sum() / len(y_pred)
    return


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