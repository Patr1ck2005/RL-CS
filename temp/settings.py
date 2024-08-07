# 调整工程宏观设置
class GlobalSettings:
    def __init__(self):
        # game.py类区
        self.tick_rate = 60  # 游戏内部更新频率
        self.time_step = 1 / self.tick_rate  # 游戏内部更新时间间隔
        # player.py类区
        self.max_speed = 4  # 最大速度
        self.max_face_vel = 1  # 最大转向速度
        self.acceleration = 0.1  # 移动命令每一个tick的加速度
        self.friction = 0.05  # 摩擦力
        self.player_size = 5  # 角色半径
        self.shoot_range = 50  # 射程
