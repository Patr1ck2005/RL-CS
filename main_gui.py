from Visual.base_visual import BaseGameGUI
from Visual.aim_training_visual import AimTrainingGUI
import pickle
import neat
import os

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, './config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

with open('./winner', 'rb') as f:
    c = pickle.load(f)
net = neat.nn.FeedForwardNetwork.create(c, config)
players = {
    'human': {'team': 'blue', 'nn': net},
    'A': {'team': 'red', 'nn': net}
}

gamegui = BaseGameGUI()
aim_training_gui = AimTrainingGUI()

if __name__ == '__main__':
    gamegui.restart_game()
    gamegui.add_players(players)
    gamegui.run()
    # aim_training_gui.restart_game()
    # aim_training_gui.add_players(players)
    # aim_training_gui.add_chickens(10)
    # aim_training_gui.run()
