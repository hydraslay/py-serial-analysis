from __future__ import print_function

import os
import neat
import evo.visualize as visualize
from evo.eval_for_para import eval_net, market_data, axis_label


def run(config_file):

    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')

    # Show output of the most fit genome against training data.
    winner_net = neat.nn.RecurrentNetwork.create(p, config)
    winner_net.reset()
    output = eval_net(winner_net, market_data(30000, 30350), verbose=True)
    print(" final balance 1: {}".format(output))

    winner_net.reset()
    output = eval_net(winner_net, market_data(30000, 30400), verbose=True)
    print(" final balance 2: {}".format(output))

    winner_net.reset()
    output = eval_net(winner_net, market_data(30000, 30450), verbose=True)
    print(" final balance 3: {}".format(output))

    visualize.draw_net(config, p, True, node_names=axis_label)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-exchange')
    run(config_path)
