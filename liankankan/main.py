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
    # 创建个大地图
    __map = [[0] * 20 for _ in range(20)]
    # 创建图标群
    icons = Group()

    screen.fill(ai_settings.bg_color)
    # 让最近绘制的屏幕可见
    pygame.display.flip()
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, icons, __map)
        if stats.game_active:
            icons.update()
            gf.clear_icons(__map, icons, -1, ai_settings, stats, screen)
        if stats.game_active != -1:
            gf.update_screen(ai_settings, screen, icons, stats, play_button)
        else:
            button = Button(ai_settings, screen, "GAME OVER!")
            gf.update_screen(ai_settings, screen, icons, stats, button)

run_game()
