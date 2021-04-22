import pygame
import sys

class Rocket():
    def __init__(self, sets, screen):
        self.screen = screen
        self.sets = sets

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('../alien_invasion/images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性 center 中存储小数值
        self.center = float(self.rect.centerx)
    def update(self):
        
        # 根据 self.center 更新 rect 对象
        self.rect.centerx = self.center

def run_game():
    pygame.init()

    screen = pygame.display.set_mode((1200,800))
    pygame.display.set_caption("rocket")

    # 创建火箭
    rocket = Rocket()

    # 游戏主循环
    while 1:
        gf.check_events(rocket)
        rock.update()
        gf.update_screen(sets, screen, rocket)
run_game()