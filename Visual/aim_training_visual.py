from Visual.base_visual import BaseGameGUI
from Game.aim_training import AimTraining
import pygame
import math


class AimTrainingGUI(BaseGameGUI, AimTraining):
    def __init__(self):
        super().__init__()

    def draw_players(self):
        super().draw_players()
        for chicken in self.chicken_list:
            name = chicken.name
            pos = self.creature_stats[name]['pos']
            pos = (pos[0] * self.s, pos[1] * self.s)  # 转换单位
            face = self.creature_stats[name]['face']
            color = 'yellow'
            if chicken.alive == 0:
                color = 'gray'
            pygame.draw.circle(self.screen, color, pos, self.settings.chicken_size)
            pygame.draw.line(self.screen, color, width=3, start_pos=pos,
                             end_pos=(pos[0] + math.cos(face) * self.settings.player_face_len,
                                      pos[1] + math.sin(face) * self.settings.player_face_len))


