import sys
import pygame
import random
from button import Button
from pygame.sprite import Group

from icon import Icon

def check_keydown_events(event, icons, ai_settings, screen, stats):
    """相应按键"""
    if event.key is pygame.K_q:
        sys.exit()
    elif event.key is pygame.K_m:
        if len(icons) != 1 :
            return
        for icon in icons:
            icons.remove(icon)
        stats.game_active = -1
        # 让最近绘制的屏幕可见
        #pygame.display.flip()
        #update_screen(ai_settings, screen, icons, stats, button)
        #pygame.rect.draw(screen, )

def check_events(ai_settings, screen, stats, play_button, icons, __map):
    """相应事件"""
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            sys.exit()
        elif event.type is pygame.KEYDOWN:
            check_keydown_events(event, icons, ai_settings, screen, stats)
        elif event.type is pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > 220 + 70 and mouse_x - 220 < 10 * 70 and mouse_y > 70 and mouse_y < 10 * 70:
                point_icon(mouse_x, mouse_y, screen, __map, stats, icons, ai_settings)
            check_play_button(stats, play_button, mouse_x, mouse_y, __map, ai_settings, screen, icons)
            

def check_play_button(stats, play_button, mouse_x, mouse_y, __map, ai_settings, screen, icons):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.game_active = 1
        stats.reset_stats()
        create_icons(ai_settings, screen, icons, __map)
        

def update_screen(ai_settings, screen, icons, stats, button):
    """ 更新屏幕上的图像,并切换到新屏幕 """
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    icons.draw(screen)

    if stats.game_active < 1:
        button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def create_icon(ai_settings, screen, icons, row_number, icon_number, num):
    icon = Icon(ai_settings, screen, num)
    icon_width = icon.rect.width
    icon.x = 220 + icon_width + icon_width * icon_number
    icon.rect.x = icon.x
    icon.rect.y = icon.rect.height + icon.rect.height * row_number
    icon.ny = row_number
    icon.nx = icon_number
    icons.add(icon)
    return icon

def create_icons(ai_settings, screen, icons, __map):
    """创建图标"""
    number_icons_x = ai_settings.game_size
    number_rows = ai_settings.game_size
    nums = get_randoms(ai_settings)
    for row_number in range(number_rows):
        for icon_number in range(number_icons_x):
            num = nums.pop()
            icon = create_icon(ai_settings, screen, icons, row_number, icon_number, num)
            __map[row_number][icon_number] = icon

def get_randoms(ai_settings):
    nums = []
    num = 0
    ns = [0, 0, 0, 0, 0, 0, 0 ,0]
    if ai_settings.game_size > 8:
        for _ in range(ai_settings.game_size ** 2 - 7):
            num = int(random.uniform(1, 9))
            nums.append(num)
    else:
        for _ in range(ai_settings.game_size ** 2 - 4):
            num = int(random.uniform(1, 6))
            nums.append(num)

    for n in nums:
        ns[n-1] += 1
    if ns[0] % 2 :
        nums.append(1)
    else:
        nums.append(5)
    if ns[1] % 2 :
        nums.append(2)
    else:
        nums.append(5)
    if ns[2] % 2 :
        nums.append(3)
    else:
        nums.append(5)
    if ns[3] % 2 :
        nums.append(4)
    else:
        nums.append(5)
    if ai_settings.game_size < 8:
        return nums
    if ns[4] % 2 :
        nums.append(5)
    else:
        nums.append(8)
    if ns[5] % 2 :
        nums.append(6)
    else:
        nums.append(8)
    if ns[6] % 2 :
        nums.append(7)
    else:
        nums.append(8)
    return nums

def point_icon(mouse_x, mouse_y, screen, __map, stats, icons, ai_settings):
    # 70 应该是icon宽度才对
    x = int((mouse_x - 220) / 70 - 1)
    y = int(mouse_y / 70 - 1)
    if __map[y][x]:
        icon = __map[y][x]
        if icon.num == -1 or stats.game_active == 0:
            return
        # 取消选择
        if icon.ok:
            print(y, x, 'False')
            point_icon_no(ai_settings, __map, icons, screen, x, y)
            return
        # 选择
        pygame.draw.rect(__map[y][x].image, (250,0,0), (0,0,70,70), 5)
        __map[y][x].ok = True
        print(y, x, icon.ok)
        #point_icon_yes(ai_settings, __map, icons, screen, x, y)
        
def point_icon_yes(ai_settings, __map, icons, screen, x, y):
    icon = __map[y][x]
    __icon = []
    for i in range(ai_settings.game_size):
        for j in range(ai_settings.game_size):
            if __map[i][j].red is True and i != x and j != y:
                icons.remove(__map[i][j])
                icons.remove(__icon[0])
                __map[i][j].num = -1
                __map[__icon[1]][__icon[2]].num = -1
                # 重建原icon
                ic_2 = create_icon(ai_settings, screen, icons, y, x, icon.num)
                __map[i][j] = ic_2
    # 选择时才调用point()
    icon.point()

def point_icon_no(ai_settings, __map, icons, screen, x, y):
    icon = __map[y][x]
    icons.remove(icon)
    # 重建原icon
    ic_2 = create_icon(ai_settings, screen, icons, y, x, icon.num)
    __map[y][x] = ic_2

def clear_icons(__map, icons, x, ai_settings, stats, screen):
    __icon = []
    for i in range(ai_settings.game_size):
        for j in range(ai_settings.game_size):
            if __map[i][j].ok is True and x != -1:
                ok = check_ok(__map, __map[i][j], __icon[0], ai_settings)
                icons.remove(__map[i][j])
                icons.remove(__icon[0])
                if not ok:
                    # 重建原icon
                    ic_2 = create_icon(ai_settings, screen, icons, i, j, __map[i][j].num)
                    __map[i][j] = ic_2
                    ic_3 = create_icon(ai_settings, screen, icons, __icon[1], __icon[2], __icon[0].num)
                    __map[__icon[1]][__icon[2]] = ic_3
                if ok:
                    __map[i][j].num = -1
                    __map[__icon[1]][__icon[2]].num = -1
                x = -1
                __map[i][j].ok = False
                __map[__icon[1]][__icon[2]].ok = False
                continue

            if __map[i][j].ok is True:
                x = __map[i][j].nx
                if __icon:
                    __icon.pop()
                    __icon.pop()
                    __icon.pop()
                __icon.append(__map[i][j])
                __icon.append(i)
                __icon.append(j)
    is_gg(__map, stats, ai_settings)
            
def check_ok(__map, p1, p2, ai_settings):
    if p1.num == p2.num:
        if straight_link(__map, p1, p2):
            return True
        if isOneCornerLink(__map, p1, p2):
            return True
        if isTwoCornerLink(__map, p1, p2, ai_settings):
            return True
    return False

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
        return 1

    point_corner.nx = p2.nx
    point_corner.ny = p1.ny
    if straight_link(__map, p1, point_corner) and straight_link(__map, point_corner, p2) and isEmptyInMap(__map, point_corner):
        return 1

def isTwoCornerLink(__map, p1, p2, ai_settings):
    for y in range(-1, ai_settings.game_size + 1):
        point_corner1 = Icon(p1.nx, y, 1)
        point_corner2 = Icon(p2.nx, y, 1)
        point_corner1.nx = p1.nx
        point_corner1.ny = y
        point_corner2.nx = p2.nx
        point_corner2.ny = y
        if y == p1.ny or y == p2.ny:
            continue
        if y == -1 or y == ai_settings.game_size:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner2, p2):
                return 1
        else:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner1, point_corner2) and straight_link(__map, point_corner2, p2) and isEmptyInMap(__map, point_corner1) and isEmptyInMap(__map, point_corner2):
                return 1

    # 横向判断
    for x in range(-1, ai_settings.game_size + 1):
        point_corner1 = Icon(x, p1.ny, 1)
        point_corner2 = Icon(x, p2.ny, 1)
        point_corner1.nx = x
        point_corner1.ny = p1.ny
        point_corner2.nx = x
        point_corner2.ny = p2.ny
        if x == p1.nx or x == p2.nx:
            continue
        if x == -1 or x == ai_settings.game_size:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner2, p2):
                return 1
        else:
            if straight_link(__map, p1, point_corner1) and straight_link(__map, point_corner1, point_corner2) and straight_link(__map, point_corner2, p2) and isEmptyInMap(__map, point_corner1) and isEmptyInMap(__map, point_corner2):
                return 1

def isEmptyInMap(__map, point):
    return __map[point.ny][point.nx].num == -1

def is_gg(__map, stats, ai_settings):
    for i in range(ai_settings.game_size):
        for j in range(ai_settings.game_size):
            icon = __map[i][j]
            if icon.num != -1:
                return
    stats.game_active = 0
    if ai_settings.game_size == 6:
        ai_settings.increase_size()
    print("game over")
