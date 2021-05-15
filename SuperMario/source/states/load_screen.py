import pygame
from .. import setup
from .. import tools
from .. import constants as C
from ..components import info

class LoadScreen:
    def __init__(self):
        pass
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'level'
        self.duration = 500 # 持续时间半秒(应该为2秒)
        self.timer = 0
        self.info = info.Info('load_screen', self.game_info)

    def update(self, surface, keys):
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration: # 计时器，加载页面停止
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.info.draw(surface)

class GameOver(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'main_menu'
        self.timer = 0
        self.duration = 1000 # 持续时间1秒(应该为4秒)
        self.info = info.Info('game_over', self.game_info)