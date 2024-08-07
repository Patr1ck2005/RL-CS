import numpy as np


class Object:
    def __init__(self, name):
        self.name = name
        self.position = None
        self.velocity = None
        self.facing = None
        self.face_vel = None
        self.goal = None

    def add_to_world(self):
        self.position = [20 * np.random.random(), 20 * np.random.random()]
        self.velocity = [0, 0]
        self.face_vel = 0  # 设置AI转向的速度
        self.facing = np.random.random() * 2 * np.pi  # 以角度计量朝向

    def physics(self):
        pass


class Creature(Object):
    def __init__(self, name):
        super().__init__(name)
        self.max_hp = 200
        self.size = 0.5
        self.hp = None
        self.deaths = None
        self.alive = None

    def spawn(self):
        super().add_to_world()
        self.hp = self.max_hp
        self.alive = True

    def check_alive(self):
        if self.hp <= 0:
            self.alive = False
        else:
            self.alive = True

    def get_states(self):
        return {'pos': self.position,
                'vel': self.velocity,
                'face': self.facing,
                'f_vel': self.face_vel,}


