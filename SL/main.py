import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch.nn import functional as F
from torch import nn
import torchvision
import numpy as np
import time

transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
dataset_train = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
dataset_validation = torchvision.datasets.MNIST(root='./data', train=False, transform=transform, download=True)

dataloader_train = DataLoader(dataset_train, batch_size=64, shuffle=True, drop_last=True)
dataloader_validation = DataLoader(dataset_validation, batch_size=64, shuffle=True, drop_last=False)


class TrainDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


class NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.module = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 10),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.module(x)
        return x


writer = SummaryWriter()

mynn = NN()
loss = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(mynn.parameters(), lr=0.01)
epoch = 100
for i in range(epoch):
    average_loss = []
    mynn.train()
    for batch in dataloader_train:
        images, labels = batch
        outputs = mynn(images)
        loss_value = loss(outputs, labels)
        optimizer.zero_grad()
        loss_value.backward()
        optimizer.step()
        average_loss.append(loss_value.item())
    mean_loss = np.mean(average_loss)
    writer.add_scalar('data/scalar', mean_loss, i)

    mynn.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for batch in dataloader_validation:
            images, labels = batch
            outputs = mynn(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        writer.add_scalar('data/validation', correct / total, i)
torch.save(mynn, 'mynn.pth')
torch.save(mynn.state_dict(), 'mynn_state_dict.pth')
writer.close()
