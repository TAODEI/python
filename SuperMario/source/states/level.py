import pygame, os, json
from .. import setup
from .. import tools
from .. import constants as C
from ..components import info, player, stuff, brick

class Level:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'game_over'
        self.info = info.Info('level', self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_positions() 
        self.setup_player()
        self.setup_ground_items()
        self.setup_bricks()

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    def setup_background(self):
        self.image_name = self.map_data['image_name'] # 减少硬编码
        self.background = setup.GRAPHICS[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI), int(rect.height * C.BG_MULTI)))
        self.background_rect = self.background.get_rect()
        # 滑动的游戏窗口
        self.game_window = setup.SCREEN.get_rect()
        # 游戏场景
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

    def setup_player(self):
        self.player = player.Player('mario')
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def setup_ground_items(self):
        self.ground_items_group = pygame.sprite.Group() # 精灵组
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_bricks(self):
        self.brick_group = pygame.sprite.Group()
        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x, y = brick_data['x'], brick_data['y']
                brick_type = brick_data['type']
                if 'brick_num' in brick_data:
                    pass
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type))        

    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)
        
        if self.player.dead:
            if self.current_time - self.player.death_timer > 1000: # 死亡时间超过一秒(应该为3秒)
                self.finished = True
                self.update_game_info()
        else:
            self.update_player_position()
            self.check_if_go_die()
            self.update_game_window()
            self.info.update()
            self.brick_group.update()

        self.draw(surface)

    def update_player_position(self):

        # x:
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x # 不超过地图左边
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x # 不超过地图右边
        self.check_x_collisions()

        # y:
        self.player.rect.y += self.player.y_vel
        self.check_y_collisions()

    def check_x_collisions(self):
        check_group = pygame.sprite.Group()

        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_x(ground_item)


    def check_y_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_y(ground_item)
        self.check_will_fall(self.player) # 悬空bug

    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x: # 从左往右碰撞
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        if self.player.rect.bottom < sprite.rect.bottom: # 从上往下碰撞
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'
        else:
            self.player.y_vel = 7
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'
        
    def check_will_fall(self, sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group)
        collided = pygame.sprite.spritecollideany(sprite, check_group)
        if not collided and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1
    
    def update_game_window(self):
        '''移动窗口来代替人物'''
        third = self.game_window.x + self.game_window.width / 3 # 三分之一之后就跟着动
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x: # 最后是不能走回头路
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x
        
    def draw(self, surface):
        self.game_ground.blit(self.background, self.game_window, self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        self.brick_group.draw(self.game_ground)

        surface.blit(self.game_ground, (0, 0), self.game_window) # 目标，左上角放在原图的位置，特定部分(默认全部)
        
        self.info.draw(surface)

    def check_if_go_die(self):
        if self.player.rect.y > C.SCREEN_H:
            self.player.go_die()

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
            self.game_info.update({ # 初始信息
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'small'
        })
        else:
            self.next = 'load_screen'