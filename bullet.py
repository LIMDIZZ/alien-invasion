import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class for controlling bullets fired by a ship"""
    def __init__(self, ai_game):
        """Creates a bullet object at the current position of the ship."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # Creating a bullet in pos (0,0) and assigning the right position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # The position of the bullet is stored in a real format
        self.y = float(self.rect.y)

    def update(self):
        """Moves the bullet up the screen"""
        # Updating the bullet position in real format
        self.y -= self.settings.bullet_speed
        # Updating the rectangle position
        self.rect.y = self.y

    def draw_bullet(self):
        """Bullet output to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
