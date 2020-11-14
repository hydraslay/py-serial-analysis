from evo.history_data import read_data
from evo.operator_mono_predictor import MonoPredictor
import neat

axis_label = {
    -1: 'high ratio',
    -2: 'low ratio',
    -3: 'close',
    -4: 'volume',
    0: 'mono',
}


csv_data = read_data()

market_inputs = csv_data[31000:32000]
eval_times = 1
bulk_size = 1000


def market_data(start, end):
    return csv_data[start: end]


def eval_net(net, ticks, verbose=False, pred=None):
    if pred is None:
        pred = MonoPredictor(1, verbose, no_predict=970)
    for market in ticks:
        pred.tick_market(market)
        input = pred.get_data()
        output = net.activate(input)
        pred.predict(output)

    return pred.calc_score(), pred


def eval_genome(genome, config):
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
