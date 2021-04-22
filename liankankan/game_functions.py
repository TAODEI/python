import sys
import pygame
#from 

def check_keydown_events(event, ai_settings, screen):
    """相应按键"""
    if event.key == pygame.K_q:
        sys.exit()

def check_events(ai_settings, screen, icons):
    """相应鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen)

def update_screen(ai_settings, screen, icons):
    """ 更新屏幕上的图像,并切换到新屏幕 """
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    #for bullet in bullets.sprites():
    for icon in icons:
        icon.draw_icon()
    #ship.blitme()

def update_icons(ai_settings, screen, icons):
    """更新图标"""

def create_icons(ai_settings, screen, icons):
    """创建图标"""
    