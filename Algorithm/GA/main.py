from Algorithm.GA.algorithm.GA import GA
from Algorithm.GA.visual.GAVisual import GAVisual
import numpy as np

mode = 'VIS'
dimension = 2
bounds = [
    [0, 10],
    [0, 10],
    [0, 10],
    [0, 10],
]


def problem(vector):
    x = vector[0]
    y = vector[1]
    return -(x - 4) ** 2 - (y - 5)**2 + 50


if __name__ == '__main__':
    if mode == 'CAL':
        GA = GA(problem, dimension, bounds)
        GA.run()
        GA.get_result()
    if mode == 'VIS':
        GAVisual = GAVisual(problem, dimension, bounds)
        GAVisual.run()
