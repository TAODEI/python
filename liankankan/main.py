import pygame
import time
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from button import Button
from time_board import Time_board
import game_functions as gf

def run_game():
    pygame.init()

    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("王者荣耀")
    
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    # 创建个大地图
    __map = [[0] * 20 for _ in range(20)]
    # 创建图标群
    icons = Group()

    #创建计时牌
    time_board = Time_board(ai_settings, screen, stats)

    screen.fill(ai_settings.bg_color)
    # 让最近绘制的屏幕可见
    pygame.display.flip()
    total_time = stats.time
    tag = 1
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, icons, __map)
        if stats.game_active:
            # 初始或过关刷新时间
            if stats.time > total_time or tag:
                total_time = stats.time
                start_time = int(time.time())
                tag = 0
            # 用时间戳更新倒计时时间
            time_board.stats.time = total_time + start_time -int(time.time())
            time_board.prep_time()

            icons.update()
            gf.clear_icons(__map, icons, -1, ai_settings, stats, screen)
        # 超时
        if time_board.stats.time == 0:
            stats.game_active = -2
        if stats.game_active == 0 or stats.game_active == 1:
            gf.update_screen(ai_settings, screen, icons, stats, play_button, time_board)
        # game_active: 1 = 正常，0 = 未开始， -1 = 通关， -2 = 超时（CAI JI）
        elif stats.game_active == -1:
            button = Button(ai_settings, screen, "GAME OVER!")
            gf.update_screen(ai_settings, screen, icons, stats, button, time_board)
        elif stats.game_active == -2:
            button = Button(ai_settings, screen, "CAI  JI")
            gf.update_screen(ai_settings, screen, icons, stats, button, time_board)
run_game()
