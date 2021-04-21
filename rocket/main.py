import pygame
import sys
from settings import Settings
from rocket import Pocket
import game_functions as gf

def run_game():
    pygame.init()

    sets = Settings()

    screen = pygame.display.set_mode(
        (sets.screen_width, sets.screen_height))
    pygame.display.set_caption("rocket")

    # 创建火箭
    rocket = Rocket(sets, screen)

    # 游戏主循环
    while 1:
        gf.check_events(rocket)
        rock.update()
        gf.update_screen(sets, screen, rocket)
run_game()