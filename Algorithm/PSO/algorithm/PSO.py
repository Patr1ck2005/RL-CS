import numpy as np
from Algorithm.algorithm import Algorithm
from Algorithm.settings import PSOSettings
import random


class PSO(Algorithm):
    def __init__(self, fitness, dimension, bounds, mode='max', n_iter=20, num_particles=30):
        super().__init__(fitness, dimension, bounds)
        settings = PSOSettings(n_iter, num_particles)
        self.n_iter = settings.n_iter
        self.num_particles = settings.num_particles
        self.w = settings.inertia_weight
        self.c1 = settings.cognitive_weight
        self.c2 = settings.social_weight
        self.r = settings.random

        self.velocity_limit = np.empty((self.dimension, 2))
        for i in range(self.dimension):
            self.velocity_limit[i][0] = -0.2
            self.velocity_limit[i][1] = 0.2

        self.particles = None
        self.velocities = None
        self.all_fitness = None
        self.iter = None

        self.social_max_value = None
        self.social_max = np.empty((1, self.dimension)).astype(np.float64)
        self.self_max_values = np.empty((self.num_particles, 1)).astype(np.float64)
        self.self_max = np.empty((self.num_particles, self.dimension)).astype(np.float64)

    def cal_times(self):
        return self.iter * self.num_particles

    def cal_all_fitness(self):
        for i in range(self.num_particles):
            self.all_fitness[i] = self.fitness(self.particles[:, i])

    def update_self(self, particle_index):
        before = self.particles
        self.self_update(particle_index)
        if self.self_max_values[particle_index] <= self.all_fitness[particle_index]:
            self.self_max_values[particle_index] = self.all_fitness[particle_index]
            self.self_max[particle_index] = self.particles[:, particle_index]
            return True
        else:
            self.particles = before
            return False

    def update_velocity(self, particle_index):
        self.velocities[:, particle_index] = \
            (self.w * self.velocities[:, particle_index]
             + self.c1 * np.random.random() * (self.social_max - self.particles[:, particle_index])
             + self.c2 * np.random.random() * (self.self_max[particle_index] - self.particles[:, particle_index]))
        for i in range(self.dimension):
            if self.velocities[i, particle_index] < self.velocity_limit[i][0]:
                self.velocities[i, particle_index] = self.velocity_limit[i][0]
            elif self.velocities[i, particle_index] > self.velocity_limit[i][1]:
                self.velocities[i, particle_index] = self.velocity_limit[i][1]

    def self_update(self, particle_index):
        self.particles[:, particle_index] += self.velocities[:, particle_index]
        for i in range(self.dimension):
            if self.particles[i, particle_index] < self.bounds[i][0]:
                self.particles[i, particle_index] = self.bounds[i][0]
            elif self.particles[i, particle_index] > self.bounds[i][1]:
                self.particles[i, particle_index] = self.bounds[i][1]

    def update_social_max(self):
        old = self.social_max_value
        for i in range(self.num_particles):
            if self.social_max_value < self.all_fitness[i]:
                self.social_max_value = self.all_fitness[i][0]
                self.social_max = self.particles[:, i]
        self.loss = self.social_max_value/old

    def get_result(self):
        self.result = self.social_max
        return self.result

    def print_info(self):
        print('social max is', self.social_max)
        print('social max value is', self.social_max_value)
        print('loss is', self.loss)

    def init(self, example=None):
        self.iter = 0
        text = 'PSO initialised'
        print(f'{text:=^20}')
        self.particles = np.empty((self.dimension, self.num_particles)).astype(np.float64)
        self.velocities = np.zeros((self.dimension, self.num_particles)).astype(np.float64)
        self.all_fitness = np.empty((self.num_particles, 1)).astype(np.float64)
        for i in range(self.dimension):
            for j in range(self.num_particles):
                self.particles[i][j] = random.uniform(self.bounds[i][0], self.bounds[i][1])
        if example is not None:
            self.particles[:, 0] = example
        print('init cal all')
        self.cal_all_fitness()

        self.social_max_value = np.max(self.all_fitness)
        self.social_max = self.particles[:, np.where(self.all_fitness == self.social_max_value)[0][0]]
        for i in range(self.num_particles):
            self.self_max[i] = self.particles[:, i]
            self.update_velocity(i)
            self.update_self(i)
        self.self_max_values = self.all_fitness

    def step(self):
        self.iter += 1
        print(f'iteration {self.iter}')
        self.cal_all_fitness()
        self.update_social_max()
        for i in range(self.num_particles):
            self.update_velocity(i)
            if self.update_self(i):
                # print(f'updated self position to {self.particles[:, i]}')
                pass
            else:
                pass
                # print(f'remain position')

    def run(self):
        self.init()
        text = 'PSO initialised'
        print(f'{text:=^20}')
        while self.iter < self.n_iter:
            self.step()
            self.print_info()
