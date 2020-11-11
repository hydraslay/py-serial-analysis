from __future__ import print_function
import numpy as np
import multiprocessing
import os
import neat
import evo.visualize as visualize
from evo.eval_binary_predict import eval_genome, eval_net, market_data, axis_label


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
    # winner = p.run(eval_genomes, 10)
    winner = p.run(pe.evaluate, 200)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nWinner:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    winner_net = neat.nn.RecurrentNetwork.create(winner, config)
    winner_net.reset()
    output, pred = eval_net(winner_net, market_data(30250, 30750), verbose=True)
    print(" final balance 1:")
    print(pred)

    visualize.plot_binary_predictions(np.array(pred.actual_history), np.array(pred.predict_history),
                                      pred.threshold, pred.no_predict, True, filename='prediction_1.svg')

    winner_net.reset()
    output, pred = eval_net(winner_net, market_data(31000, 31500), verbose=True)
    print(" final balance 2:")
    print(pred)
    visualize.plot_binary_predictions(np.array(pred.actual_history), np.array(pred.predict_history),
                                      pred.threshold, pred.no_predict, True, filename='prediction_2.svg')

    winner_net.reset()
    output, pred = eval_net(winner_net, market_data(31500, 32000), verbose=True)
    print(" final balance 3:")
    print(pred)
    visualize.plot_binary_predictions(np.array(pred.actual_history), np.array(pred.predict_history),
                                      pred.threshold, pred.no_predict, True, filename='prediction_3.svg')

    visualize.draw_net(config, winner, True, node_names=axis_label)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-binary-predict')
    run(config_path)
