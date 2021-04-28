import pygame.font
class Time_board():

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 100)

        self.prep_time()

    def prep_time(self):
        """ 将时间转换为一幅渲染的图像 """
        time_str = str(self.stats.time)
        self.time_image = self.font.render(time_str, True, self.text_color, self.ai_settings.bg_color)
        # 将得分放在屏幕右上角
        self.time_rect = self.time_image.get_rect()
        self.time_rect.right = self.screen_rect.right - 40
        self.time_rect.top = 40

    def show_time(self):
        self.screen.blit(self.time_image, self.time_rect)








class decTime(object):
    #将秒转化为时分秒
    def __init__(self,totalTime):
        self.sec = totalTime
        self.minute = int(self.sec / 60)
        self.sec = int(self.sec % 60)
    #时间减   
    def subTime(self):
        if self.sec > 0:
            self.sec -=  1
        else:
            if self.minute > 0:
                self.minute -= 1
                self.sec = 59