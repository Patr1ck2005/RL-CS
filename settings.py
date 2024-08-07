import math


# 调整工程宏观设置
class GlobalSettings:
    def __init__(self):
        # game.py类区
        self.tick_rate = 60    # 游戏内部更新频率
        self.time_step = 1/self.tick_rate    # 游戏内部更新时间间隔
        self.shoot_range = 1000

        # player.py类区
        self.max_speed = 4    # 最大速度
        self.max_face_vel = 5  # 最大转向速度
        self.acceleration = 0.1    # 移动命令每一个tick的加速度
        self.friction = 0.05    # 摩擦力
        self.shoot_range = 50  # 射程
        self.player_size = 0.5
        self.bullet_damage = 20
        self.reaction = 3
        self.fov = 180*math.pi/180
        self.fov_step = 60
        self.fov_delta = self.fov/self.fov_step

        # chicken
        self.chicken_size = 0.3

        # nn.py类区
        self.n_layer = 3
        self.n_hidden_network = [30]
        self.n_input = 60
        self.n_output = 1

