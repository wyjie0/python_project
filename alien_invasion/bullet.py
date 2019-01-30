import pygame
from pygame.sprite import Sprite
"""使用Sprite可以将游戏中相关的元素编组，进而同时操作编组中的所有元素"""

class Bullet(Sprite):
    """一个对飞机发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, jet):
        """在飞机所处的位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen

        #在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = jet.rect.centerx
        self.rect.top = jet.rect.top
        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        # self.space_down = False

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y


    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)