class Settings:
    """Class for storing all settings of the Alien Invasion game"""
    def __init__(self):
        """Inits static game settings"""
        # screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 0, 0)

        # ship
        self.ship_limit = 2

        # bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 6

        # alien
        self.fleet_drop_speed = 10

        # Speed up the game
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inits the settings changing during the game"""
        self.ship_speed = 3
        self.alien_speed = 3
        self.bullet_speed = 3
        # 1 indicates movement to the right and -1 to the left
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increases speed settings"""
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
