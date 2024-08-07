# 导入游戏主程序，用于多玩家对象的交互
from Game.game import *
from Algorithm.deep_learing import *
from settings import *


class Player:
    def __init__(self, name, team):
        global_settings = GlobalSettings()
        self.name = name
        self.team = team
        self.brain = Brain()
        self.time_step = global_settings.time_step
        self.max_v = global_settings.max_speed
        self.max_fv = global_settings.max_face_vel
        self.size = global_settings.player_size
        self.bullet_damage = global_settings.bullet_damage
        self.reaction = global_settings.reaction

        # 静态属性
        self.goals = None
        self.assists = None
        self.kills = None
        self.deaths = None
        self.hp = None
        self.damage = None
        self.weapon = None
        self.ammo = None
        self.alive = None
        self.trigger = None
        # 动态属性 需要输入神经网络
        self.know = None
        self.position = None
        self.velocity = None
        self.facing = None
        self.face_vel = None
        self.fire = None
        self.view = None

    # 初始化
    def init(self):
        self.goals = 0
        self.alive = True
        self.assists = 0
        self.kills = 0
        self.deaths = 0
        self.hp = 100
        self.damage = 0
        self.weapon = 'AK'
        self.ammo = 30

        self.position = [10, 10]
        self.velocity = [0, 0]
        self.face_vel = 1   # 设置AI转向的速度
        self.facing = 0     # 以角度计量朝向
        self.fire = 0    # 作为判断是否开火
        self.view = []

    def command(self, command):
        # 根据指令设置速度（指令约等于加速度
        self.velocity[0] += command['a_x']
        self.velocity[1] += command['a_y']
        self.face_vel += command['a_f']

    def v_limit(self):
        # 拙劣地限制速度，建议点击左边隐藏
        if self.velocity[0] > self.max_v:
            self.velocity[0] = self.max_v
        elif self.velocity[0] < -self.max_v:
            self.velocity[0] = -self.max_v
        if self.velocity[1] > self.max_v:
            self.velocity[1] = self.max_v
        elif self.velocity[1] < -self.max_v:
            self.velocity[1] = -self.max_v
        if self.face_vel > self.max_fv:
            self.face_vel = self.max_fv
        elif self.face_vel < -self.max_fv:
            self.face_vel = -self.max_fv

    # 射击函数
    def shoot(self):
        self.ammo -= 1
        self.fire = 1
        self.damage += self.bullet_damage

    def hold_trigger(self):
        self.trigger = self.reaction

    # 每次射击后重置射击
    def reset_fire(self):
        self.fire = 0

    def check(self):
        if self.hp <= 0:
            self.deaths += 1
            self.alive = False
            self.team = 'gray'
            print('dead')

    def get_info(self, info):
        self.know = info

    def think(self):
        self.brain.get_inputs(self.know)
        self.brain.run()
        act = self.brain.get_outputs()
        self.velocity = act['vel']
        self.face_vel = act['f_vel']
        # self.fire = act['fire']   # 简化为自动开枪

    # 移动更新函数
    def step(self):
        self.v_limit()
        self.position[0] += self.velocity[0] * self.time_step
        self.position[1] += self.velocity[1] * self.time_step
        self.facing += self.face_vel * self.time_step

    def get_hit(self):
        self.hp -= self.bullet_damage
        self.check()

    def get_states(self):
        return {'pos': self.position,
                'vel': self.velocity,
                'face': self.facing,
                'f_vel': self.face_vel,
                'fire': self.fire,
                'team': self.team}

