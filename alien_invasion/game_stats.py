class GameStats:
    """
    跟踪游戏的统计信息
    """
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        #在任何情况下都不应该重置最高得分
        with open("high_score",'r',encoding='utf-8') as f_obj:
            content = f_obj.read()
            if content:
                self.high_score = int(content)
            else:
                self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.jets_left = self.ai_settings.jet_limit
        self.score = 0
        self.level = 1