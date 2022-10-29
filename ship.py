import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Class for controlling a ship"""
    def __init__(self, ai_game):
        """Init the ship and its start position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Loading the ship image and the rect
        self.image = pygame.image.load('images/characters/spaceship.png')
        self.rect = self.image.get_rect()
        # Every new ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        # Saving the real coordinate of the center of the ship
        self.x = float(self.rect.x)
        # Move flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updates the position of the ship taking into account the flag"""
        # x attribute is updated, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Updating the rect attribute based on self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draws a ship in the current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
