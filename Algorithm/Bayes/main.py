from algorithm.SMBO import *
import numpy as np


bounds = {
    'x': (0, 10),
    'y': (0, 10)
}


def problem(x, y):
    return -(x-4)**2-(y-5)**2+50


if __name__ == '__main__':
    opt = BayesOpt(problem, bounds, n_iter=100)
    result = opt.run()
    print(result)

