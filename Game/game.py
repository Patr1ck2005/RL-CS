# 导入玩家类
import numpy as np
from Object.player import Player
from settings import *
import math
import random


class BaseGameRule:
    def __init__(self):
        global_settings = GlobalSettings()
        self.tick_rate = global_settings.tick_rate
        self.shoot_range = global_settings.shoot_range
        self.player_size = global_settings.player_size
        self.tick = None
        self.players_list = []
        self.creature_list = []
        self.creature_stats = {}
        # 区别人类对象
        self.human = None

    # 初始化游戏程序并且添加玩家对象
    def restart_game(self):
        self.tick = 0
        self.players_list = []
        self.creature_stats = {}

    def spawn_all(self):
        self.spawn_players()

    def add_players(self, players_dict):
        for name in players_dict:
            team = players_dict[name]['team']
            nn = players_dict[name]['nn']
            player = Player(name, team, neat_nn=nn)
            self.players_list.append(player)
            if name == 'human':
                self.human = player
        self.creature_list = self.players_list

    def spawn_players(self, mode='random'):
        for player in self.players_list:
            player.spawn()

    def see_and_shoot(self, player):
        x, y = player.position
        face = player.facing % (2*math.pi)
        for other_creature in self.creature_list:
            if not other_creature == player and other_creature.alive:
                ax, ay = other_creature.position
                if ax != x and ay != y:
                    angle = math.atan2(ay-y, ax-x)
                    if angle < 0:
                        angle += 2*math.pi
                    dis = math.sqrt((ax-x)**2+(ay-y)**2)
                    size = other_creature.size
                    delta = math.atan(size/dis)
                    Delta = player.fov/2
                    # 视野范围
                    if face-Delta <= angle <= face+Delta:
                        # if face > np.pi:
                        #     face_temp = face - 2*np.pi
                        # else:
                        #     face_temp = face
                        relative_angle = angle-face
                        if relative_angle > np.pi:
                            relative_angle = relative_angle-2*np.pi
                        if relative_angle < -np.pi:
                            relative_angle = relative_angle+2*np.pi
                        player.saw_enemy(relative_angle)
                        # print(player.name, 'saw', other_creature.name)
                    # 判断是否扣动扳机
                    if dis <= self.shoot_range and angle-delta <= face <= angle+delta:
                        if player.trigger is None:
                            player.hold_trigger()
                        else:
                            player.trigger -= 1
                        if player.trigger == 0:
                            player.fire = 1
                            player.shoot()
                            # print(f'{player.name} shoot {other_creature.name}')
                            other_creature.get_hit()
                            player.trigger = None

    # 主循环
    def step(self):
        self.tick += 1
        for player in self.players_list:
            if player.alive:
                if player.fire:
                    player.reset_fire()
                player.reset_vision()
                self.see_and_shoot(player)
                player.step()
        for creature in self.creature_list:
            # 主程序备份状态
            self.creature_stats[creature.name]: dict = creature.get_states()

    def get_result(self):
        result = {}
        for player in self.players_list:
            result[player.name] = player.get_goals()
        print(result)
        return result

    def game_over(self):
        self.creature_stats = {}


# 测试草稿区域
if __name__ == '__main__':
    pass
