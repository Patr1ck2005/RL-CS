import numpy as np


class Settings:
    def __init__(self):
        pass


class PSOSettings:
    def __init__(self, n_iter=20, num_particles=30):
        self.n_iter = n_iter
        self.num_particles = num_particles
        self.inertia_weight = 0.75
        self.cognitive_weight = 0.2
        self.social_weight = 0.2
        self.random = 0.4


class GASettings:
    def __init__(self, n_generations=20, population_size=30):
        self.n_generations = n_generations
        self.population_size = population_size
        self.mutation_rate = 0.1
        self.crossover_rate = 0.5
        self.elite_proportion = 0.1
        self.mutation_type = 'genetic'

        # self.selection_type = 'tournament'
        # self.tournament_size = 3
        # self.crossover_type = 'uniform'
        # self.mutation_probability = 0.1
        # self.elitism_size = 1

