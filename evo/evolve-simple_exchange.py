from __future__ import print_function

import multiprocessing
import os
import neat
import evo.visualize as visualize
from evo.eval_simple_exchange import eval_genome, eval_net, market_data, axis_label


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        eval_genome(genome, config)


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to N generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count() - 1, eval_genome)
    winner = p.run(pe.evaluate, 1000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nWinner:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    winner_net = neat.nn.RecurrentNetwork.create(winner, config)
    winner_net.reset()
    output, acc = eval_net(winner_net, market_data(2880, 4320), verbose=True)
    print(" final balance 1:")
    print(acc)

    winner_net.reset()
    output, acc = eval_net(winner_net, market_data(4320, 5760), verbose=True)
    print(" final balance 2:")
    print(acc)

    winner_net.reset()
    output, acc = eval_net(winner_net, market_data(4320, 7200), verbose=True)
    print(" final balance 3:")
    print(acc)

    visualize.draw_net(config, winner, True, node_names=axis_label)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-simple_exchange')
    run(config_path)
