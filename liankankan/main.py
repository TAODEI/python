import pygame
from pygame.sprite import Group
from settings import Settings
import game_functions as gf

def run_game():
    pygame.init()

    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("连看看")

    icons = Group()
    # 创建图标群
    gf.create_icons(ai_settings, screen, icons)

    while 1:
        gf.check_events(ai_settings, screen, icons)
        gf.update_icons(ai_settings, screen, icons)
        gf.update_screen(ai_settings, screen, icons)

run_game()
