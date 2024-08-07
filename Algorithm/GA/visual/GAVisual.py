import random

import pygame as pg
from Algorithm.GA.algorithm.GA import GA


class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (30, 30, 30)
        self.axe_color = (0, 0, 0)
        self.fps = 1


class GAVisual(GA):
    def __init__(self, problem, dimension, bounds):
        super().__init__(problem, dimension, bounds)
        settings = Settings()
        self.scale = 80
        self.WIDTH = settings.screen_width
        self.HEIGHT = settings.screen_height
        self.screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
        self.axe = pg.Surface(((self.bounds[0][1] - self.bounds[0][0]) * self.scale,
                               (self.bounds[1][1] - self.bounds[1][0]) * self.scale))
        self.clock = pg.time.Clock()
        self.bg_color = settings.bg_color
        self.axe_color = settings.axe_color
        self.fps = settings.fps

    def init(self):
        pg.init()
        pg.display.set_caption('Visualization of GA')

    def update(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.axe, (0, 0))
        self.axe.fill(self.axe_color)
        self.draw_info()
        pg.draw.circle(self.axe, (255, 0, 255), (4 * self.scale, 5 * self.scale), 10)
        for i in range(self.population_size):
            self.draw_obj(i)
        pg.display.update()
        self.clock.tick(self.fps)

    def draw_obj(self, i):
        pixel_pos = [self.decode_all()[i][j] * self.scale for j in range(2)]
        pg.draw.circle(self.axe, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                       pixel_pos, 5*random.uniform(0.5, 1))
        # self.draw_bg()

    def draw_bg(self):
        i = 0
        j = 0
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                color_value = self.fitness((i / self.scale, j / self.scale)) * (-0.001)
                color = (int(255*color_value), int(255*color_value), int(255*color_value))
                self.axe.set_at((i, j), color)

    # 在左上角标识出迭代次数
    def draw_info(self):
        text_1 = "Generation: " + str(self.generation)
        text_2 = "Cal times: " + str(self.cal_times())
        text_3 = "Best fitness: " + str(round(max(self.all_fitness), 3))
        font = pg.font.SysFont(None, 30)
        text_surface_1 = font.render(text_1, True, (255, 255, 255))
        text_surface_2 = font.render(text_2, True, (255, 255, 255))
        text_surface_3 = font.render(text_3, True, (255, 255, 255))
        self.screen.blit(text_surface_1, (10, 10))
        self.screen.blit(text_surface_2, (10, 40))
        self.screen.blit(text_surface_3, (10, 70))

    def run(self):
        self.init()
        GA.init(self)
        while True:
            self.reproduction()
            self.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()