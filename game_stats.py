import json


class GameStats:
    """Statistics for the Alien Invasion game"""
    def __init__(self, ai_game):
        """Init the stats"""
        self.settings = ai_game.settings
        self.reset_stats()
        # The Alien Invasion game starts in the non-active state
        self.game_active = False
        # High score should never be reset
        self.high_score = self.save_high_score()

    def save_high_score(self):
        """Gets high score from file if it exists"""
        try:
            with open('high_score.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0

    def reset_stats(self):
        """Init the stats that change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
