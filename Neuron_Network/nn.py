import torch
import torch.nn as nn
import torch.nn.functional as F


# a nn with 60 input and 1 hidden layer and 1 output
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(60, 1)

    def forward(self, x):
        x = self.fc1(x)
        return x
