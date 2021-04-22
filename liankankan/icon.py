import pygame
from pygame.sprite import Sprite

class Icon(Sprite):
    __gameSize = 10 # 游戏尺寸
    __iconKind = __gameSize * __gameSize / 4 # 小图片种类数量
    __iconWidth = 40
    __iconHeight = 40

    def __init__(self, ai_settings, screen):
        super(Icon, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载图标,并设置其 rect 属性
        
        '''提取小头像数组'''
        self.image = pygame.image.load('images/icon.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        #root_dir = os.getcwd()
#imagePath = os.path.join(root_dir, 'images', 'NARUTO.png')
#imageSouce = Image.open(imagePath)
        for index in range(0, int(self.__iconKind)):
            region = self.image.crop((self.__iconWidth * index, 0, 
            self.__iconWidth * index + self.__iconWidth - 1, self.__iconHeight - 1))
            icons.append(ImageTk.PhotoImage(region))