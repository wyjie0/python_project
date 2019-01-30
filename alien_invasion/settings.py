'''
    游戏的设置模块
    用于存储所有的设置，以免在代码中到处添加设置
    使函数调用更简单，在项目增大时修改游戏的外观更加容易
    要修改游戏，只需修改settings.py中的一些值，无需查找散布在文件中的不同设置
'''
class Settings:

    """存储所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置
        self.name = 'Alien Invasion'
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230,230,230)
        #对话框设置
        self.diag_width = 70
        self.diag_height = 30
        self.diag_color = (255,255,255)
        #飞机设置
        # self.jet_speed_factor = 1.5
        self.jet_limit = 3
        #子弹设置
        # self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        #外星人设置
        # self.alien_speed_factor = 1.5
        # self.fleet_drop_speed = 50
        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.2
        #外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.jet_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        #记分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人点数"""
        self.jet_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)
        # print(self.alien_points)