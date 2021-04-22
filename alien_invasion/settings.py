class Settings():
    """ 存储《外星人入侵》的所有设置的类 """
    def __init__(self):
        """ 初始化游戏的设置 """
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (100, 200, 230)

        # 飞船的设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed_factor = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 6, 6, 6
        self.bullets_allowed = 10

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 30
        self.fleet_direction = 1

        