import numpy as np
from settings import *
import matplotlib.pyplot as plt
import time


class NeuronNetwork:
    def __init__(self, all_w, all_b):
        settings = GlobalSettings()
        self.know = None
        self.act = None

        self.n_layer = settings.n_layer
        self.n_hidden_nn: list = settings.n_hidden_network
        self.n_input = 1
        self.n_output = 3

        self.all_w: list = all_w
        self.all_b: list = all_b

    def relu(self, x):
        return np.maximum(x, 0)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def forward(self, a, w, b):
        z_forward = w.T @ a + b
        a_forward = self.tanh(z_forward)
        return a_forward

    def get_inputs(self, inputs):
        self.know = inputs

    def run(self, inputs):
        a0 = inputs
        for i in range(0, self.n_layer-1):
            a0 = self.forward(a0, self.all_w[i], self.all_b[i])
        self.act = self.tanh(a0)[0][0]

    def get_outputs(self):
        return self.act


if __name__ == '__main__':
    all_w = [np.load('../datas/all/all_w_0.npy'), np.load('../datas/all/all_w_1.npy')]
    all_b = [np.load('../datas/all/all_b_0.npy'), np.load('../datas/all/all_b_1.npy')]
    # all_w = [np.random.uniform(-1, 1, (60, 30)), np.random.uniform(-1, 1, (30, 1))]
    # all_b = [np.random.uniform(-1, 1, (30, 1)), np.random.uniform(-1, 1, (1, 1))]
    nn = NeuronNetwork(all_w, all_b)
    test = np.zeros((60, 1))
    out_put = []
    for i in range(60):
        test[i] = 1
        nn.run(test)
        test[i] = 0
        print(nn.get_outputs())
        out_put.append(nn.get_outputs())
    plt.plot(out_put)
    plt.show()
