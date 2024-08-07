# pip3 install gym
# pip3 install neat-python

# for gym stuff:
# apt install xvfb ffmpeg xorg-dev libsdl2-dev swig cmake
# pip3 install gym[box2d]

import multiprocessing
import os
import pickle

import neat
import numpy as np

from Game.game import BaseGameRule

# ====================================================================
runs_per_net = 100

game = BaseGameRule()


# Use the NN network phenotype and the discrete actuator force function.

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitnesses = []
    players = {
        'p1': {'team': 'red', 'nn': net},
        'p2': {'team': 'blue', 'nn': net}
    }
    for runs in range(runs_per_net):
        game.restart_game()
        game.add_players(players)
        for i in range(100):
            game.step()
        fitness = game.get_result()['p1']
        # game.game_over()
        fitnesses.append(fitness)

    return np.mean(fitnesses)


# ====================================================================


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, './config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)


if __name__ == '__main__':
    run()
