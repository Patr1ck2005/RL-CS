import numpy as np
import math


class Algorithm:

    def __init__(self, problem, dimension, bounds):
        self.fitness = problem
        self.dimension = dimension
        self.bounds = bounds
        self.result = None
        self.loss = None


