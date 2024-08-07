# 导入玩家类
from Object.player import *
from Object.player import Player
from settings import *
import math
import random


class MainProgramme:
    def __init__(self):
        global_settings = GlobalSettings()
        self.tick_rate = global_settings.tick_rate
        self.shoot_range = global_settings.shoot_range
        self.player_size = global_settings.player_size
        self.tick = None
        self.players = []
        self.player_names = []
        self.player_stats = {}
        self.players_in_fire = []
        # 区别人类对象
        self.human = None

    # 初始化游戏程序并且添加玩家对象
    def init(self, player_names: tuple = ('A', 'human')):
        self.tick = 0
        self.player_names = player_names
        # 判断人类玩家
        for name in player_names:
            if name == 'human':
                self.human = Player(name, 'blue')
                self.players.append(self.human)
            else:
                self.players.append(Player(name, 'red'))
            welcome = f'{name} join the map'
            print(f'{welcome:=^20}')  # 格式化字符串打印提示信息
        # 初始化玩家对象（设置位置等参数
        for player in self.players:
            player.restart_game()

    def shoot_attack(self, player):
        x, y = player.position
        face = player.facing % (2*math.pi)
        for other_player in self.players:
            if not other_player == player:
                ax, ay = other_player.position
                if ax != x or ay != y:
                    angle = math.atan2((ay-y), ax-x)
                    if angle < 0:
                        angle += 2*math.pi
                    dis = math.sqrt((ax-x)**2+(ay-y)**2)
                    size = other_player.size
                    delta = math.atan(size/dis)
                    if dis <= self.shoot_range and angle-delta <= face <= angle+delta:
                        if player.trigger is None:
                            player.hold_trigger()
                        else:
                            player.trigger -= 1
                        if player.trigger == 0:
                            player.fire = 1
                            player.shoot()
                            other_player.get_hit()
                            player.trigger = None

    # 存活检测
    def check_alive(self,player):
        if not player.alive:
            self.players.remove(player)

    # 主循环
    def step(self):
        self.tick += 1
        self.players_in_fire = []
        for player in self.players:
            player.step()
            self.watch(player)
            self.shoot_attack(player)
            if player.fire:
                # 设置开火玩家列表
                self.players_in_fire.append(player)
                player.reset_fire()
            #   判断是否产生命中
            #   self.shoot_attack(player)
            self.check_alive(player)
            # 主程序备份玩家状态
            self.player_stats[player.name]: dict = player.get_states()


# 测试草稿区域
if __name__ == '__main__':
    pass
