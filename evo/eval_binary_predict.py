from evo.history_data import read_data
from evo.operator_binary_predictor import BinaryPredictor
import neat

axis_label = {
    -1: 'open(5m)',
    -2: 'high(5m)',
    -3: 'low(5m)',
    -4: 'close(5m)',
    -5: 'volume(5m)',
    -6: 'open(1h)',
    -7: 'high(1h)',
    -8: 'low(1h)',
    -9: 'close(1h)',
    -10: 'volume(1h)',
    0: 'next_1',
    1: 'next_2',
    2: 'next_3',
    3: 'next_4',
}


csv_data = read_data()

market_inputs = csv_data[30000:31000]
eval_times = 1
bulk_size = 500


def market_data(start, end):
    return csv_data[start: end]


def eval_net(net, ticks, verbose=False):
    pred = BinaryPredictor(verbose)
    for market in ticks:
        pred.tick_market(market)
        input = pred.get_data()
        output = net.activate(input)
        pred.predict(output)

    return pred.calc_score(), pred


def eval_genome(genome, config):
    # print('eval_genome start {}'.format(genome.key))
    genome.fitness = -1
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
