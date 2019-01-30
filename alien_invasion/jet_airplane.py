import pygame
from pygame.sprite import Sprite
class JetAirplane(Sprite):
    """初始化飞机并设置其初始位置"""
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.hp = 3

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load("images/jet_airplane.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将没搜新飞机放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞机的属性center中存储小数值
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        #根据飞机的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.ai_settings.jet_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center_x -= self.ai_settings.jet_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.center_y -= self.ai_settings.jet_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.ai_settings.jet_speed_factor

        #根据self.center_x和self.center_y跟新rect对象
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

    def center_jet(self):
        """让飞船在屏幕上居中"""
        self.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        self.screen.blit(self.image,self.rect)