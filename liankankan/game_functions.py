import sys
import pygame
import random
from icon import Icon

def check_keydown_events(event, icons, ai_settings, screen):
    """相应按键"""
    if event.key is pygame.K_q:
        sys.exit()
    elif event.key is pygame.K_m:
        #for event in pygame.event.get():
            #if event.key is pygame.K_u:
            #if event.key is pygame.K_x:
             #   if event.key is pygame.K_i:
        if len(icons) != 1 :
            return
        for icon in icons:
            icons.remove(icon)

def check_events(ai_settings, screen, icons, __map):
    """相应事件"""
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            sys.exit()
        elif event.type is pygame.KEYDOWN:
            check_keydown_events(event, icons, ai_settings, screen)
        elif event.type is pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > 220 + 70 and mouse_x - 220 < 10 * 70 and mouse_y > 70 and mouse_y < 10 * 70:
                point_icon(mouse_x, mouse_y, icons, screen, __map)

def update_screen(ai_settings, screen, icons):
    """ 更新屏幕上的图像,并切换到新屏幕 """
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    #for bullet in bullets.sprites():
    #for icon in icons:
    #   icon.draw_icon()
    #ship.blitme()
    icons.draw(screen)
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def create_icon(ai_settings, screen, icons, icon_number, row_number, num):
    icon = Icon(ai_settings, screen, num)
    icon_width = icon.rect.width
    icon.x = 220 + icon_width + icon_width * icon_number
    icon.rect.x = icon.x
    icon.rect.y = icon.rect.height + icon.rect.height * row_number
    icon.nx = row_number
    icon.ny = icon_number
    icons.add(icon)
    return icon

def create_icons(ai_settings, screen, icons, __map):
    """创建图标"""
    number_icons_x = 9
    number_rows = 9
    num = 0
    for row_number in range(number_rows):
        for icon_number in range(number_icons_x):
            num = int(random.uniform(1, 6))
            #num = (row_number + icon_number) % 5 + 1
            icon = create_icon(ai_settings, screen, icons, icon_number, row_number, num)
            __map[row_number][icon_number] = icon

def update_icons(ai_settings, screen, icons):
    """更新图标"""
    icons.update()

def point_icon(mouse_x, mouse_y, icons, screen, __map):
    # 70 应该是icon宽度才对
    y = int((mouse_x - 220) / 70 - 1)
    x = int(mouse_y / 70 - 1)
    if __map[x][y]:
        __map[x][y].point()
        print(x, y, __map[x][y].ok)

def clear_icons(__map, icons, x, y):
    __icon = []
    for i in range(9):
        for j in range(9):
            icon = __map[i][j]
        #for icon in __map[i]:
            if icon.ok is True and x != -1:
                ok = check_ok(__map, icon, __icon[0])
                if ok:
                    icons.remove(icon)
                    icons.remove(__icon[0])
                    #__map[i].remove(icon)
                    __map[i][j].num = -1
                    #__map[__icon[1]].remove(__icon[0])
                    __map[__icon[1]][__icon[2]].num = -1
                    icon.ok = False
                    __icon[0].ok = False
                    x = -1
                    print("ok")
                    print(i)
                    continue
                icon.ok = False
                __icon[0].ok = False
            if icon.ok is True:
                x = icon.nx
                y = icon.ny
                if __icon:
                    __icon.pop()
                    __icon.pop()
                    __icon.pop()
                __icon.append(icon)
                __icon.append(i)
                __icon.append(j)
            
def check_ok(__map, p1, p2):
    ok = 0
    if p1.num == p2.num:
        if straight_link(__map, p1, p2):
            ok = 1
        if isOneCornerLink(__map, p1, p2):
            ok = 1
        if isTwoCornerLink(__map, p1, p2):
            ok = 1
    return ok

def straight_link(__map, p1, p2):
    start = -1
    end = -1
    # 水平
    if p1.ny == p2.ny:
        # 大小判断
        if p2.nx < p1.nx:
            start = p2.nx
            end = p1.nx
        else:
            start = p1.nx
            end = p2.nx
        for x in range(start + 1, end):
            if __map[p1.ny][x].num != -1:
                return False
        return True
    elif p1.nx == p2.nx:
        if p1.ny > p2.ny:
            start = p2.ny
            end = p1.ny
        else:
            start = p1.ny
            end = p2.ny
        for y in range(start + 1, end):
            if __map[y][p1.nx].num != -1:
                return False
        return True
    return False

def isOneCornerLink(__map, p1, p2):
    point_corner = Icon(p1.nx, p2.ny, 1)
    point_corner.nx = p1.nx
    point_corner.ny = p2.ny
    if straight_link(__map, p1, point_corner) and straight_link(__map, point_corner, p2) and isEmptyInMap(__map, point_corner):
        #return point_corner
        return 1

    point_corner = Icon(p2.nx, p1.ny, 1)
    point_corner.nx = p2.nx
    point_corner.ny = p1.ny
    if straight_link(__map, p1, point_corner) and straight_link(__map, point_corner, p2) and isEmptyInMap(__map, point_corner):
        return 1 #point_corner

def isTwoCornerLink(__map, p1, p2):
    for y in range(-1, 9 + 1):
        point_corner1 = Icon(p1.nx, y, 1)
        point_corner2 = Icon(p2.nx, y, 1)
        point_corner1.nx = p1.nx
        point_corner1.ny = y
        point_corner2.nx = p2.nx
        point_corner2.ny = y
        if y == p1.ny or y == p2.ny:
            continue
        if y == -1 or y == 9:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner2, p2):
                return 1 #{'p1': point_corner1, 'p2': point_corner2}
        else:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner1, point_corner2) and straight_link(__map, point_corner2, p2) and isEmptyInMap(__map, point_corner1) and isEmptyInMap(__map, point_corner2):
                return 1 #{'p1': point_corner1, 'p2': point_corner2}

    # 横向判断
    for x in range(-1, 9 + 1):
        point_corner1 = Icon(x, p1.ny, 1)
        point_corner2 = Icon(x, p2.ny, 1)
        point_corner1.nx = x
        point_corner1.ny = p1.ny
        point_corner2.nx = x
        point_corner2.ny = p2.ny
        if x == p1.nx or x == p2.nx:
            continue
        if x == -1 or x == 9:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner2, p2):
                return {'p1': point_corner1, 'p2': point_corner2}
        else:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner1, point_corner2) and straight_link(__map, point_corner2, p2) and isEmptyInMap(__map, point_corner1) and isEmptyInMap(__map, point_corner2):
                return {'p1': point_corner1, 'p2': point_corner2}

def isEmptyInMap(__map, point):
    if __map[point.ny][point.nx].num == -1:
        return True
    else:
        return False
