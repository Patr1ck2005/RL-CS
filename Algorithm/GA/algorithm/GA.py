import numpy as np
from Algorithm.algorithm import Algorithm
from Algorithm.settings import GASettings
import random
import copy
import time
import math


class GA(Algorithm):
    def __init__(self, problem, dimension, bounds, gene_num=10, n_generations=20, population_size=50):
        super().__init__(problem, dimension, bounds)
        settings = GASettings(n_generations, population_size)
        self.max_generations = settings.n_generations
        self.population_size = settings.population_size
        self.mutation_rate = settings.mutation_rate
        self.crossover_rate = settings.crossover_rate
        self.elite_proportion = settings.elite_proportion
        self.mutation_type = settings.mutation_type

        self.chromosome_num: int = dimension
        if type(gene_num) == int:
            self.gene_num = [gene_num for i in range(self.chromosome_num)]
        else:
            self.gene_num: list = gene_num
        self.elites_num = int(self.population_size * self.elite_proportion)+1
        self.generation = None
        self.population_DNA = []
        self.elites_DNA = []
        self.best_DNA = []
        self.all_fitness = []

        self.err = 0.1

    def cal_times(self):
        return self.generation * self.population_size

    def cal_fitness(self, x):
        if x > 0:
            return x
        else:
            return 0
        # return 1/(1+math.exp(-x))

    def encode(self, values):
        codes = []
        for i, value in enumerate(values):
            code = []
            a = self.bounds[i][0]
            b = self.bounds[i][1]
            order = int((2**self.gene_num[i]-1)*(value-a)/(b-a))
            while order > 0:
                bit = order % 2
                code.append(bit)
                order = order // 2
            while len(code) < self.gene_num[i]:
                code.append(0)
            codes.append(code)
        return codes

    def decode(self, codes):
        values = []
        for i, code in enumerate(codes):
            a = self.bounds[i][0]
            b = self.bounds[i][1]
            values.append(a + (b - a) / (2 ** self.gene_num[i] - 1)
                          * sum([num * 2 ** index for index, num in enumerate(code)]))
        return values

    def decode_all(self):
        return [self.decode(DNA) for DNA in self.population_DNA]

    def init(self, example=None):
        self.generation = 0
        self.population_DNA = [[[random.randint(0, 1) for i in range(self.gene_num[j])]
                                for j in range(self.chromosome_num)]
                               for k in range(self.population_size)]
        if example is not None:
            self.population_DNA[0] = self.encode(example)
        text = 'GA initialised'
        print(f'{text:=^20}')

    def evaluate_all(self):
        self.all_fitness = [self.cal_fitness(self.fitness(self.decode(DNA)))
                            for DNA in self.population_DNA]

    def mutation_chromosome(self, chromosome):
        if random.random() < self.mutation_rate:
            chromosome[random.randint(0, self.gene_num - 1)] = random.randint(0, 1)

    def mutation_gene(self, chromosome, index):
        # print('in mutation func:')
        for i in range(self.gene_num[index]):
            if random.random() < self.mutation_rate:
                chromosome[i] = random.randint(0, 1)
                # print('mutate in ', i)
        # print('mutated loc to', chromosome)

    def crossover(self, chromosome1, chromosome2, index):
        # print('before\t', chromosome1, chromosome2)
        cut = sorted([random.randint(0, self.gene_num[index] - 1) for i in range(2)])
        if random.random() < 0.5:
            re = 1
        else:
            re = -1
        chromosome1 = chromosome1[:cut[0]] + chromosome2[cut[0]:cut[1]] + chromosome1[cut[1]:]
        chromosome2 = chromosome2[:cut[0]] + chromosome1[cut[0]:cut[1]] + chromosome2[cut[1]:]
        # print('after\t', chromosome1, chromosome2)
        return chromosome1, chromosome2

    def mutate_all(self):
        # print('='*30)
        for i in range(self.population_size):
            for j in range(self.chromosome_num):
                if self.mutation_type == 'genetic':
                    # print(f'in loc: {i}{j}')
                    # print('before m', self.population_DNA)
                    self.mutation_gene(self.population_DNA[i][j], j)
                    # print('after m chromosome is')
                    # print(f'population_DNA[{i}][{j}]', self.population_DNA[i][j])
                    # print('after m all DNA is')
                    # print(f'population_DNA', self.population_DNA)
                elif self.mutation_type == 'chromosome':
                    self.mutation_chromosome(self.population_DNA[i][j])
        # print('after')
        # print(self.population_DNA)

    def crossover_elites(self, selection):
        for i in selection:
            for j in range(self.chromosome_num):
                if random.random() < self.crossover_rate:
                    temp = random.randint(0, self.population_size - 1)
                    chromosome1 = self.population_DNA[i][j]
                    chromosome2 = self.population_DNA[temp][j]
                    self.population_DNA[i][j], self.population_DNA[temp][j] \
                        = self.crossover(chromosome1, chromosome2, j)

    def select(self):
        selection = []
        total = sum(self.all_fitness)
        accumulation = [sum(self.all_fitness[:i + 1]) / total for i in range(self.population_size)]
        rand_list = sorted([random.random() for i in range(self.population_size)])
        i = 0
        j = 0
        while j < self.population_size:
            if rand_list[j] < accumulation[i]:
                selection.append(i)
                j += 1
            else:
                i += 1
        return selection

    def reproduction(self):
        self.generation += 1
        print(f'generation {self.generation}')
        old_best = self.all_fitness[0] if self.generation > 1 else None
        self.evaluate_all()

        sorted_zip = zip(self.all_fitness, self.population_DNA)
        sorted_zip = sorted(sorted_zip, key=lambda x: -x[0])
        self.all_fitness,  self.population_DNA = zip(*sorted_zip)
        self.all_fitness = list(self.all_fitness)
        self.population_DNA = list(self.population_DNA)
        self.best_DNA = copy.deepcopy(self.population_DNA[0])
        self.loss = self.all_fitness[0]/old_best if self.generation > 1 else None

        self.elites_DNA = copy.deepcopy(self.population_DNA[:self.elites_num])
        self.population_DNA[-self.elites_num:] = copy.deepcopy(self.elites_DNA)

        self.crossover_elites(self.select())
        self.mutate_all()
        self.population_DNA[0] = copy.deepcopy(self.best_DNA)

    def get_result(self):
        self.result = self.decode(self.best_DNA)
        print('best is ', self.result)
        return self.result

    def print_info(self):
        print('best is ', self.decode(self.best_DNA))
        print('best fitness is', self.all_fitness[0])
        print('loss is', self.loss)

    def run(self):
        self.init()
        text = 'GA initialised'
        print(f'{text:=^20}')
        while self.generation < self.max_generations:
            self.reproduction()
            self.print_info()
            # self.print_info()


if __name__ == '__main__':
    # lst = []
    # time_start = time.time()
    # lst_1 = [random.uniform(0, 10) for i in range(1000000)]
    # lst_2 = [random.uniform(0, 10) for i in range(1000000)]
    lst_3 = []
    array_1 = np.zeros(10000000)
    for i in range(10000000):
        lst_3.append(i)

    t1 = time.time()
    for i in range(10000000):
        lst_3[i] = i
    t2 = time.time()
    for i in range(10000000):
        array_1[i] = i
    t3 = time.time()
    print(t2 - t1)
    print(t3 - t2)
    # time_mid = time.time()
    # array = np.random.uniform(0, 10, 1000000)
    # lst_3 = [i+j for i, j in zip(lst_1, lst_2)]

    # time_end = time.time()
    # array_1 = np.array(lst_1)
    # array_2 = np.array(lst_2)
    #     # for i in range(1000000):)
    # array_3 = array_1 + array_2
    # lst.append(random.randint(0, 10))
    # array[i] = random.uniform(0, 10)
    # array0 = np.append(array0, random.randint(0, 10))
    # print(time_mid - time_start)
    # print(time_end - time_mid)

