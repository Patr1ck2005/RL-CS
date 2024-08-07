import math
import random


class Temperature:
    def __init__(self):
        self.temperature = None

    def heat(self):
        self.temperature = 10

    def cold(self):
        self.temperature -= 1

    def random(self):
        if random.random() > 0.5:
            return True
        else:
            return False
