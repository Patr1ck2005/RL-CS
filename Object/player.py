from Neuron_Network.numpy_nn import *
from settings import *
import time
import math
from Object.object import Creature


class Player(Creature):
    def __init__(self, name, team, neat_nn=None):
        super().__init__(name)
        global_settings = GlobalSettings()
        self.team = team
        # neat 神经网络
        self.neat_brain = neat_nn

        self.time_step = global_settings.time_step
        self.max_v = global_settings.max_speed
        self.max_fv = global_settings.max_face_vel
        self.size = global_settings.player_size
        self.bullet_damage = global_settings.bullet_damage
        self.reaction = global_settings.reaction
        self.fov = global_settings.fov
        self.fov_step = global_settings.fov_step
        self.fov_delta = global_settings.fov_delta

        # 静态属性
        self.assists = None
        self.kills = None
        self.damage = 0
        self.weapon = None
        self.ammo = 30
        self.trigger = None
        # 动态属性 需要输入神经网络
        self.vision = {'enemy': np.zeros((self.fov_step, 1)),
                       'allies': None,
                       'wall': None}
        self.fire = None

    # 初始化
    def init(self):
        self.alive = True
        self.assists = 0
        self.kills = 0
        self.deaths = 0
        self.hp = 100000
        self.damage = 0
        self.weapon = 'AK'
        self.ammo = 30

        self.position = [20*np.random.random(), 20*np.random.random()]
        self.velocity = [0, 0]
        self.face_vel = 0   # 设置AI转向的速度
        self.facing = np.random.random()*2*math.pi     # 以角度计量朝向
        self.fire = 0    # 作为判断是否开火

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

    def reset_vision(self):
        self.vision = {'enemy': np.zeros((self.fov_step, 1)),
                       'allies': None,
                       'wall': None}

    def get_info(self, info):
        pass

    def saw_enemy(self, angle):
        abs_relative_angle = angle+self.fov/2
        tick = int(abs_relative_angle/self.fov_delta)
        # print(tick)
        self.vision['enemy'][tick] = 1

    def think(self):
        # self.brain.get_inputs(self.know)
        # self.velocity = act['vel']
        # self.fire = act['fire']   # 简化为自动开枪
        if self.name == 's1mple':
            tick = np.where(self.vision['enemy'] == 1)[0]
            if tick < 30:
                self.face_vel = -5
            else:
                self.face_vel = 5
        else:
            # self.brain.run(self.vision['enemy'])
            # act = self.brain.get_outputs()
            # neat神经网络实现
            observation = list(self.vision['enemy'].T)[0]
            act = self.neat_brain.activate(observation)[0]
            self.face_vel = 1*act

    # 更新函数：包含思考，位移更新，角度更新
    def step(self):
        self.think()
        self.v_limit()
        self.position[0] += self.velocity[0] * self.time_step
        self.position[1] += self.velocity[1] * self.time_step
        self.facing += self.face_vel * self.time_step

    def get_hit(self):
        self.hp -= self.bullet_damage
        self.check_alive()

    def get_states(self):
        return {'pos': self.position,
                'vel': self.velocity,
                'face': self.facing,
                'f_vel': self.face_vel,
                'fire': self.fire,
                'team': self.team}

    def get_goals(self):
        self.goals = self.damage
        return self.goals


if __name__ == '__main__':
    lst = []
    lst1 = lst
    lst.append(1)
    lst2 = [1]
    print(lst+lst2)
    print(lst1)
