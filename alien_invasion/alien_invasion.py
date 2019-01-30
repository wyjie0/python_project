"""
    程序运行的主逻辑
"""
import pygame
from settings import Settings
from game_stats import GameStats
from jet_airplane import JetAirplane
from button import Button
# from bullet import
# from alien import Alien
from scoreboard import Scoreboard
from pygame.sprite import Group
import game_functions as gf

def run_game():
    #初始化pygame、设置和屏幕对象

    pygame.init()#初始化背景

    ai_settings = Settings()#实例化设置对象
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    sb = Scoreboard(ai_settings, screen, stats)
    pygame.display.set_caption(ai_settings.name)
    #实例化飞机对象
    jet = JetAirplane(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建外星人
    aliens = Group()
    gf.create_fleet(ai_settings, screen, jet, aliens)
    #创建一个button实例
    play_button = Button(ai_settings,screen,"Start Now!")
    dialog_button = Button(ai_settings,screen,"You Lose!")
    #开始游戏主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,jet,
                        aliens,bullets)#根据事件监视来确定飞机的移动
        if stats.game_active:
            jet.update()#飞机位置的变化由飞机对象来控制
            gf.update_bullets(ai_settings,screen,stats,sb,jet,aliens,
                              bullets)
            gf.update_aliens(ai_settings,stats,screen,sb,jet,aliens,bullets)
        # else:
        #
        #     break
        # aliens.update()
        # print(len(bullets))
        #每次循环时都重绘屏幕,与更新屏幕有关的内容都在update_screen()中
        gf.update_screen(ai_settings, screen, stats, sb, jet, bullets, aliens,
                         play_button)

run_game()