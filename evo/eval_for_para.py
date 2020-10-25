from evo.operator_breaker import Account
import os
import pandas as pd
import neat
import numpy as np

initial_fund = 10000

axis_label = {
    -1: 'balance',
    -2: 'pos(buy)',
    -3: 'cost(buy)',
    -4: 'pos(sell)',
    -5: 'cost(sell)',
    -6: 'open(5m)',
    -7: 'high(5m)',
    -8: 'low(5m)',
    -9: 'close(5m)',
    -10: 'volume(5m)',
    -11: 'open(15m)',
    -12: 'high(15m)',
    -13: 'low(15m)',
    -14: 'close(15m)',
    -15: 'volume(15m)',
    -16: 'open(1h)',
    -17: 'high(1h)',
    -18: 'low(1h)',
    -19: 'close(1h)',
    -20: 'volume(1h)',
    0: 'tp(buy)',
    1: 'tp(sell)',
    2: 'order(buy)',
    3: 'order(sell)',
    4: 'amount(2^3)',
    5: 'amount(2^2)',
    6: 'amount(2^1)',
    7: 'amount(2^0)',
}

def read_data():
    filename_train = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY_Train.csv')
    if os.path.exists(filename_train):
        csv_data_train = pd.read_csv(filename_train, header=None, delimiter=',')
        return csv_data_train.values
    else:
        filename = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY5.csv')
        csv_data_5 = pd.read_csv(filename, header=None, delimiter=',')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY15.csv')
        csv_data_15 = pd.read_csv(filename, header=None, delimiter=',')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY60.csv')
        csv_data_60 = pd.read_csv(filename, header=None, delimiter=',')

        csv_data = merge_data(csv_data_15.values, csv_data_60.values, 5)
        csv_data = merge_data(csv_data_5.values, csv_data, 10)
        print('data ready')
        # slice to ignore 1~2 column (timestamp)
        csv_data = csv_data[:, 2:]
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


csv_data = read_data()

market_inputs = csv_data[30000:30300]
eval_times = 3
bulk_size = 150
max_drop_rate = 0.75


def market_data(start, end):
    return csv_data[start: end]


def eval_net(net, ticks, verbose=False):
    balance = initial_fund
    acc = Account(verbose)
    acc.set_balance(balance)
    for market in ticks:
        acc.tick_market(market)
        input = acc.get_data()
        output = net.activate(input)
        balance = acc.act(output)
        if balance < initial_fund * max_drop_rate:
            return balance
    return balance


def eval_genome(genome, config):
    # print('eval_genome start {}'.format(genome.key))
    genome.fitness = initial_fund
    # net = neat.nn.FeedForwardNetwork.create(genome, config)
    net = neat.nn.RecurrentNetwork.create(genome, config)
    min_fitness = -1
    start = 0
    end = start + bulk_size
    keep_going = True
    while keep_going:
        ticks = market_inputs[start: end]
        for _ in range(eval_times):
            net.reset()
            fitness = eval_net(net, ticks)
            min_fitness = fitness if fitness < min_fitness or min_fitness == -1 else min_fitness
            if min_fitness < initial_fund * max_drop_rate:
                keep_going = False
                break
        if end == len(market_inputs):
            keep_going = False
        else:
            # next bulk
            start += bulk_size
            end = start + bulk_size
            if end > len(market_inputs):
                start = len(market_inputs) - bulk_size
                end = start + bulk_size

    genome.fitness = min_fitness
    # print('eval_genome done {}'.format(genome.key))
    return genome.fitness
