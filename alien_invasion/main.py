import pygame
import sys
from settings import Settings
from ship import Ship 
import game_functions as gf

def run_game():
    # 初始化 pygame 、设置和屏幕对象
    pygame.init()
    
    ai_settings = Settings()
   
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # 创建飞船
    ship = Ship(ai_settings, screen)

    # 开始游戏主循环
    while True:
        gf.check_events(ship)
        ship.update()
        gf.update_screen(ai_settings, screen, ship)
run_game()