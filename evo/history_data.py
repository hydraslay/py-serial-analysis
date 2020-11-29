import os
import pandas as pd
import numpy as np


def read_data():
    filename_train = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY_Train.csv')
    if os.path.exists(filename_train):
        csv_data_train = pd.read_csv(filename_train, header=None, delimiter=',')
        return csv_data_train.values
    else:
        filename = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY5.csv')
        csv_data_5 = pd.read_csv(filename, header=None, delimiter=',')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY60.csv')
        csv_data_60 = pd.read_csv(filename, header=None, delimiter=',')

        csv_data = merge_data(csv_data_5.values, csv_data_60.values, 5)
        print('data ready')
        # slice to ignore 1~2 column (timestamp)
        csv_data = csv_data[:, 2:]
        np.savetxt(filename_train, csv_data, delimiter=',', fmt='%.18f')
        return csv_data


def read_one_data():
    filename_train = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY_Train.csv')
    if os.path.exists(filename_train):
        csv_data_train = pd.read_csv(filename_train, header=None, delimiter=',')
        return csv_data_train.values
    else:
        filename = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY5.csv')
        csv_data_5 = pd.read_csv(filename, header=None, delimiter=',')
        print('data ready')
        # slice to ignore 1~2 column (timestamp)
        csv_data = csv_data_5[:, 2:]
        np.savetxt(filename_train, csv_data, delimiter=',', fmt='%.18f')
        return csv_data


def merge_data(hi_freq, lo_freq, add_column):
    # add 3 columns to left
    hi_freq = np.pad(hi_freq, ((0, 0), (0, add_column)), mode='constant', constant_values=0)
    first_row = -1
    for row in range(lo_freq.shape[0]):
        lo_col_1 = lo_freq[row, 0]
        lo_col_2 = lo_freq[row, 1]
        if row == lo_freq.shape[0] - 1:
            mask = (hi_freq[:, 0] >= lo_col_1) & (hi_freq[:, 1] >= lo_col_2)
        else:
            lo_col_1_next = lo_freq[row+1, 0]
            lo_col_2_next = lo_freq[row+1, 1]
            mask = ((hi_freq[:, 0] == lo_col_1) & (hi_freq[:, 0] == lo_col_1_next) &
                    (hi_freq[:, 1] >= lo_col_2) & (hi_freq[:, 1] < lo_col_2_next))
        found_rows = np.column_stack(np.where(mask))
        if len(found_rows) > 0:
            # copy lo_freq to hi_freq
            hi_freq[mask, 7:] = lo_freq[row, 2:]
            if first_row == -1:
                first_row = found_rows[0, 0]

    return hi_freq[first_row:, :]

