"""
    存放大量让游戏运行的函数
    避免alien_invasion文件太长
    使alien_invasion文件只运行游戏的主逻辑
"""
import sys
import pygame

# from jet_airplane import JetAirplane
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,stats,jet,aliens,
                         bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        jet.moving_right = True
        # print(event.key)
    elif event.key == pygame.K_LEFT:
        jet.moving_left = True
    elif event.key == pygame.K_p:
        start_game(ai_settings,screen,stats,jet,aliens,bullets)
    #     print(event.key)
    # elif event.key == pygame.K_UP:
    #     jet.moving_up = True
    #     # print(event.key)
    # elif event.key == pygame.K_DOWN:
    #     jet.moving_down = True
        # print(event.key)
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,jet,bullets)

def check_keyup_events(event,jet):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        jet.moving_right = False
        # print(event.key)
    elif event.key == pygame.K_LEFT:
        jet.moving_left = False
        # print(event.key)
    # elif event.key == pygame.K_UP:
    #     jet.moving_up = False
    #     # print(event.key)
    # elif event.key == pygame.K_DOWN:
    #     jet.moving_down = False
        # print(event.key)
    # elif event.key == pygame.K_SPACE:
    #     for bullet in bullets:
    #         bullet.space_down = False

def start_game(ai_settings,screen,stats,jet,aliens,bullets):
    """开始游戏"""
    ai_settings.initialize_dynamic_settings()
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    # 创建一群新的外新人，并让飞船居中
    create_fleet(ai_settings, screen, jet, aliens)
    jet.center_jet()

def check_play_button(ai_settings,screen,stats,sb,play_button,jet,
                      aliens,bullets,mouse_x,mouse_y):
    """再玩家单击play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings,screen,stats,jet,aliens,bullets)
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_jets()

def check_events(ai_settings,screen,stats,sb,play_button,jet,aliens,
                 bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("high_score",'w+',encoding='utf-8') as f_obj:
                content = f_obj.read()
                if content:
                    if stats.high_score > int(content):
                        f_obj.write(stats.high_score)
                if not content:
                    f_obj.write(str(stats.high_score))
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,jet,aliens,
                         bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,jet)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,
                              jet,aliens,bullets,mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, sb, jet, bullets, aliens,
                  play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    jet.blitme()
    aliens.draw(screen)
    sb.show_score()
    #如果游戏处于非活动状态，就显示Play按钮
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,jet,aliens,bullets):
    """相应子弹和外星人的碰撞"""
    #删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, jet, aliens)
        #如果整群外星人被消灭，就提高一个等级
        stats.level += 1
        sb.prep_level()

def update_bullets(ai_settings,screen,stats,sb,jet,aliens,bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,jet,
                                  aliens,bullets)

def check_fleet_edges(ai_settings, aliens):
    """有外星人达到边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def jet_hit(ai_settings, stats, screen, sb,jet, aliens, bullets):
    """响应被外星人撞到的飞机"""
    if stats.jets_left > 0:
        #将jet_left减1
        stats.jets_left -= 1
        # print(stats.jets_left)
        # jet = JetAirplane(ai_settings, screen)
        #更新记分牌
        sb.prep_jets()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞创放到屏幕底端中央
        create_fleet(ai_settings, screen, jet, aliens)
        jet.center_jet()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, jet, aliens,
                        bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            jet_hit(ai_settings,stats,screen,sb,jet,aliens,bullets)
            break

def update_aliens(ai_settings,stats,screen,sb,jet,aliens,bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人
    :param aliens:
    :return:
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人和飞机之间的碰撞
    if pygame.sprite.spritecollideany(jet, aliens):
        # if jet.hp < 0:
        jet_hit(ai_settings,stats,screen,sb,jet,aliens,bullets)
        # jet.hp = 3
        # else:
        #     jet.hp -= 1
        # print("Jet hit!!!")
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,stats,screen,sb,jet,aliens,bullets)

def fire_bullet(ai_settings, screen, jet, bullets):
    #创建一颗子弹，并将其加入到编组bullets中
    new_bullet = Bullet(ai_settings,screen, jet)
    # new_bullet.space_down = True
    bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings, jet_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height-
                         (3*alien_height) - jet_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, jet, aliens, alien_number,
                 row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width + 6
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number \
                    + jet.rect.height/5
    aliens.add(alien)

def create_fleet(ai_settings, screen, jet, aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, jet.rect.height,
                                  alien.rect.height)
    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, jet, aliens, alien_number,
                         row_number)

def check_high_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()