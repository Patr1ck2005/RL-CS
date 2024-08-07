import numpy as np
from Algorithm.PSO.algorithm.PSO import PSO
from Algorithm.PSO.visual.PSOVisual import PSOVisual

mode = 'VIS'
dimension = 2
bound = np.empty((dimension, 2))
for i in range(dimension):
    bound[i][0] = 0
    bound[i][1] = 10


def problem(vector):
    x = vector[0]
    y = vector[1]
    return -(x - 4) ** 2-(y - 5)**2+50


if __name__ == '__main__':
    if mode == 'CAL':
        PSO = PSO(problem, dimension, bound)
        PSO.run()
    if mode == 'VIS':
        PSOVisual = PSOVisual(problem, dimension, bound)
        PSOVisual.run()

