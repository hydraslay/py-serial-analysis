from __future__ import print_function
import numpy as np
import multiprocessing
import os
import glob
import neat
import evo.visualize as visualize
from evo.eval_mono_predict import eval_genome, eval_net, market_data, axis_label


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        eval_genome(genome, config)


def run(config_file):
    max_gen = 0
    prefix = 'neat-checkpoint-'
    for filename in glob.glob(prefix + '*'):
        gen = int(filename[len(prefix):])
        max_gen = gen if gen > max_gen else max_gen

    if max_gen > 0:
        # load checkpoint
        p = neat.Checkpointer.restore_checkpoint((prefix + '{}').format(max_gen))
    else:
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
    p.add_reporter(neat.Checkpointer(10))

    # Run for up to N generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count() - 1, eval_genome)
    # winner = p.run(eval_genomes, 10)
    winner = p.run(pe.evaluate, 101)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nWinner:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    winner_net = neat.nn.RecurrentNetwork.create(winner, p.config)
    winner_net.reset()

    output, pred = eval_net(winner_net, market_data(31000, 32000), verbose=True)
    print(" trained prediction:")
    print(pred)
    print(" expended prediction:")
    output, pred = eval_net(winner_net, market_data(32000, 32030), verbose=True, pred=pred)
    print(pred)
    # print(len(pred.predict_history))
    # print(pred.predict_history[pred.no_predict:])
    visualize.plot_mono_predictions(pred.direction, np.array(pred.actual_history), np.array(pred.predict_history),
                                    pred.threshold, pred.no_predict, True, filename='prediction_ext.svg')

    visualize.draw_net(p.config, winner, False, node_names=axis_label)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-mono-predict')
    run(config_path)
