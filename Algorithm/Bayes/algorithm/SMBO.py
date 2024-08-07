from bayes_opt import BayesianOptimization
import numpy as np


class BayesOpt(object):
    def __init__(self, f, bounds, init_points=5, n_iter=25):
        self.f = f
        self.bounds = bounds
        self.init_points = init_points
        self.n_iter = n_iter
        self.bo = None

    def run(self):
        if self.bo is None:
            self.bo = BayesianOptimization(f=self.f, pbounds=self.bounds)
        self.bo.maximize(init_points=self.init_points, n_iter=self.n_iter)
        return self.bo.max['params']
