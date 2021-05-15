import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h)).convert() # 图层 方便碰撞检测
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name