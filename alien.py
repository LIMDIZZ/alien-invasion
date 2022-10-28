import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class representing a single alien"""

    def __init__(self, ai_game):
        """Initializes the alien and sets its initial position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Uploading an alien image and assigning the rect attribute
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # Every new alien in the upper left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Save the exact horizontal position of the alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """True if alien at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Moves the alien to the right or to the left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
