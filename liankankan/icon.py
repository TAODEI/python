import pygame
from pygame.sprite import Sprite

class Icon(Sprite):

    def __init__(self, ai_settings, screen, num):
        super(Icon, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.num = num
        self.ok = False
        self.nx = 0
        self.ny = 0

        # 加载图标,并设置其 rect 属性
        '''提取小头像数组'''
        if num <= 3:
            self.image = pygame.image.load('images/'+ str(num) +'.jpg')
        else:
            self.image = pygame.image.load('images/'+ str(num) +'.jpeg')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
    
    def point(self):
        pygame.draw.rect(self.image, (250,0,0), (0,0,70,70), 5)
        self.ok = True

    def blitme(self):
        self.screen.blit(self.image, self.rect)
