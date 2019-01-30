import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load("images\game_alien1.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #每个外星人初始在屏幕顶部左上角
        self.rect.x = self.rect.width
        self.rect.y = self.screen_rect.top-self.rect.height-50

        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    def update(self):
        """向左或向右移动外星人"""
        self.x += self.ai_settings.alien_speed_factor * \
                    self.ai_settings.fleet_direction

        self.rect.x = self.x
    def blitme(self):
        self.screen.blit(self.image,self.rect)