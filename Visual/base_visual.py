import pygame
from Game.game import *
import math
import sys

all_w = [np.load('datas/all/all_w_0.npy'), np.load('datas/all/all_w_1.npy')]
all_b = [np.load('datas/all/all_b_0.npy'), np.load('datas/all/all_b_1.npy')]
manual_all_w = [np.load('datas/best/all_w_0.npy'), np.load('datas/best/all_w_1.npy')]
manual_all_b = [np.load('datas/best/all_b_0.npy'), np.load('datas/best/all_b_1.npy')]


# pygameGUI相关设置
class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.player_size = 7
        self.chicken_size = 5
        self.player_face_len = 14
        self.bullet_size = 3
        self.bullet_last = 0.1
        self.scale = 20
        self.bg_color = (230, 230, 230)
        self.player_color = (255, 0, 0)
        self.bullet_color = (0, 0, 0)
        self.fire_color = (255, 0, 0)
        self.wall_color = (60, 60, 60)
        self.gui_color = (0, 255, 255)
        self.fps = 60


class BaseGameGUI(BaseGameRule):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.s = self.settings.scale
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.fire_list = []
        self.game_active = False
        self.game_over = False
        # 人类玩家特定称呼

    def draw_all(self):
        self.draw_static()
        self.draw_move()

    def draw_move(self):
        self.draw_players()

    def draw_static(self):
        # 画背景
        self.screen.fill(self.settings.bg_color)
        self.draw_gui()
        self.draw_wall()

    def draw_players(self):
        for player in self.players_list:
            name = player.name
            pos = self.creature_stats[name]['pos']
            pos = (pos[0]*self.s, pos[1]*self.s)  # 转换单位
            face = self.creature_stats[name]['face']
            color = self.creature_stats[name]['team']
            if not player.alive:
                color = 'gray'
            pygame.draw.circle(self.screen, color, pos, self.settings.player_size)
            pygame.draw.line(self.screen, color, width=3, start_pos=pos,
                             end_pos=(pos[0]+math.cos(face)*self.settings.player_face_len,
                                      pos[1]+math.sin(face)*self.settings.player_face_len))
            if player.fire == 1:
                print('fire')
                # 画子弹轨迹
                b_len = 300
                pygame.draw.line(self.screen, self.settings.bullet_color, width=2, start_pos=pos,
                                 end_pos=(pos[0] + math.cos(face) * b_len,
                                          pos[1] + math.sin(face) * b_len))
                # 画枪口火焰
                f_len = 20
                pygame.draw.line(self.screen, self.settings.fire_color, width=20, start_pos=pos,
                                 end_pos=(pos[0] + math.cos(face) * f_len,
                                          pos[1] + math.sin(face) * f_len))

    def draw_gui(self):
        pass

    def draw_wall(self):
        pass

    def mix_command(self):
        # 定义键盘指令用于测试，实现多命令的混合输入
        keys = pygame.key.get_pressed()
        command = []
        if keys[pygame.K_w]:
            command.append((0, -1, 0))
        if keys[pygame.K_s]:
            command.append((0, 1, 0))
        if keys[pygame.K_a]:
            command.append((-1, 0, 0))
        if keys[pygame.K_d]:
            command.append((1, 0, 0))
        if command:
            sum_command = {'a_x': sum([i[0] for i in command]),
                           'a_y': sum([i[1] for i in command]),
                           'a_f': sum([i[2] for i in command])}
            self.human.command(sum_command)

    def human_shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        pos = self.creature_stats['human']['pos']
        angle = math.atan2(mouse_pos[1]-pos[1]*self.s, mouse_pos[0]-pos[0]*self.s)
        self.human.face_vel = 0
        self.human.facing = angle
        self.human.shoot()

    # 主循环
    def run(self):
        while True:
            self.clock.tick(self.settings.fps)
            for event in pygame.event.get():
                self.mix_command()
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    # 按SPACE元神启动
                    if event.key == pygame.K_SPACE:
                        self.spawn_all()
                        self.game_active = True
                        print('Game Re-Start')
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.human_shoot()
            if self.game_active:
                self.step()
                self.draw_all()
                pygame.display.update()

