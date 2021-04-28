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
    #reds = Group()
    #gf.create_icons(ai_settings, screen, icons, __map)
    #image0 = Icon(ai_settings, screen, 1)
    #str1 = '\x71' * 70 * 70
    #image0.image = pygame.image.fromstring(str1.encode(), (70,70), 'P' )
    #image0.rect = image0.image.get_rect()
    #image0.rect.x = image0.rect.width
    #image0.rect.y = image0.rect.height

    #image0.x = float(image0.rect.x)
    #icons.add(image0)
    button = Button(ai_settings, screen, "GAME OVER!")
    screen.fill(ai_settings.bg_color)

    button.draw_button()
        # 让最近绘制的屏幕可见
    pygame.display.flip()
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, icons, __map)
        if stats.game_active:
            icons.update()
            gf.clear_icons(__map, icons, -1, ai_settings, stats, screen)
        gf.update_screen(ai_settings, screen, icons, stats, play_button)

run_game()
