import pygame
from pygame.sprite import Group
from settings import Settings
from icon import Icon
import game_functions as gf

def run_game():
    pygame.init()

    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("连看看")
    
    # 游戏地图
    #__map = gf.create_map(ai_settings, screen)
    
    # 创建图标群
    __map = [[0] * 9 for _ in range(9)]
    icons = Group()
    gf.create_icons(ai_settings, screen, icons, __map)

    while True:
        #gf.update_map(ai_settings, screen, __map, icons)
        x = -1
        y = -1
        gf.clear_icons(__map, icons, x, y)
        gf.check_events(ai_settings, screen, icons, __map)
        gf.update_icons(ai_settings, screen, icons)
        gf.update_screen(ai_settings, screen, icons)

run_game()
