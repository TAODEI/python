import pygame
from pygame.sprite import Group
from settings import Settings
from icon import Icon
from game_stats import GameStats
from button import Button
import game_functions as gf

def run_game():
    pygame.init()

    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("连看看")
    
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)

    # 游戏地图
    #__map = gf.create_map(ai_settings, screen)
    
    # 创建图标群
    __map = [[0] * 9 for _ in range(9)]
    icons = Group()
    #gf.create_icons(ai_settings, screen, icons, __map)

    while True:
        #gf.update_map(ai_settings, screen, __map, icons)
        x = -1
        gf.check_events(ai_settings, screen, stats, play_button, icons, __map)

        if stats.game_active:
            gf.update_icons(ai_settings, screen, icons)
            gf.clear_icons(__map, icons, x, ai_settings, stats)
        gf.update_screen(ai_settings, screen, icons, stats, play_button)

run_game()
