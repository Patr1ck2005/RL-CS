from Game.game import BaseGameRule
from Object.player import Player
from Object.chicken import Chicken


class AimTraining(BaseGameRule):
    def __init__(self):
        super().__init__()
        self.chicken_list = []

    def restart_game(self):
        super().restart_game()
        self.chicken_list = []

    def spawn_all(self):
        super().spawn_players()
        self.spawn_chickens()

    def add_chickens(self, n_chicken):
        for i in range(n_chicken):
            chicken = Chicken(name=i)
            self.chicken_list.append(chicken)
        self.creature_list = self.players_list+self.chicken_list

    def spawn_chickens(self):
        for chicken in self.chicken_list:
            chicken.spawn()

