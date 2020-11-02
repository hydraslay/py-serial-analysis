from evo.history_data import read_data
from evo.operator_breaker import Account
import neat

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


csv_data = read_data()

market_inputs = csv_data[30000:30300]
eval_times = 2
bulk_size = 300
max_drop_rate = 0.75
max_margin_rate = 0.25


def market_data(start, end):
    return csv_data[start: end]


def eval_net(net, ticks, verbose=False):
    acc = Account(initial_fund, max_margin_rate, verbose)
    for market in ticks:
        acc.tick_market(market)
        if acc.busted:
            return -1, acc
        input = acc.get_data()
        output = net.activate(input)
        acc.act(output)
        if acc.error:
            return -1, acc

    return acc.evaluate(), acc


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
            fitness, _ = eval_net(net, ticks)
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
