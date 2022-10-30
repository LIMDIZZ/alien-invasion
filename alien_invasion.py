import json
import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Resource management and game behaviour"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # Creating an instance to store game statistics
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # backgrounds
        self.bg1 = pygame.image.load('images/backgrounds/1.jpg')
        self.bg2 = pygame.image.load('images/backgrounds/2.jpg')
        self.bg3 = pygame.image.load('images/backgrounds/3.jpg')
        self.bg4 = pygame.image.load('images/backgrounds/4.jpg')
        self.bg5 = pygame.image.load('images/backgrounds/5.jpg')
        self.bg6 = pygame.image.load('images/backgrounds/6.jpg')
        self.bg7 = pygame.image.load('images/backgrounds/7.jpg')
        self.bg8 = pygame.image.load('images/backgrounds/8.jpg')
        self.bg9 = pygame.image.load('images/backgrounds/9.jpg')
        self.bg10 = pygame.image.load('images/backgrounds/10.jpg')
        self.bg11 = pygame.image.load('images/backgrounds/11.jpg')
        self.bg12 = pygame.image.load('images/backgrounds/12.jpg')
        self.bg13 = pygame.image.load('images/backgrounds/13.jpg')
        self.bg14 = pygame.image.load('images/backgrounds/14.jpg')
        self.bg15 = pygame.image.load('images/backgrounds/15.jpeg')
        self.bg16 = pygame.image.load('images/backgrounds/16.jpg')
        self.bg17 = pygame.image.load('images/backgrounds/17.jpg')
        self.bg18 = pygame.image.load('images/backgrounds/18.jpg')
        self.bg19 = pygame.image.load('images/backgrounds/19.jpg')
        self.bg20 = pygame.image.load('images/backgrounds/20.jpg')

        self._create_fleet()
        # Creating a Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Game's main cycle"""
        while True:
            self._check_events()
        # The screen is redrawn every time the cycle passes
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _update_bullets(self):
        """Updates bullet positions and destroys old bullets"""
        # Updating bullet positions
        self.bullets.update()
        self._check_bullet_alien_collisions()
        self._bullet_remover()

    def _bullet_remover(self):
        """Removing bullet that have gone beyond the edge of the screen"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_aliens_bottom(self):
        """Checks if the aliens have reached the bottom edge of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # The same as during the collision with a ship
                self._ship_hit()
                break

    def _ship_hit(self):
        """Handles the collision of a ship with an alien"""
        if self.stats.ships_left > 0:
            # Reducing ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clearing alien and bullet lists
            self.aliens.empty()
            self.bullets.empty()

            # Creating a new fleet and placing the ship in the center
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_bullet_alien_collisions(self):
        """Handling collisions of bullets with aliens"""
        # Removing bullets and aliens involved in collisions
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destruction of existing bullets and creation of a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self._start_new_level()

    def _start_new_level(self):
        # Increase level
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """Updates the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        # Checking for "alien — ship" collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Check if the aliens have reached the bottom edge of the screen
        self._check_aliens_bottom()

    def _check_events(self):
        """Handles keystrokes and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Launches a new game when the Play button is pressed"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """Starts a new game"""
        # Reset the game settings
        self.settings.initialize_dynamic_settings()

        # Reset game statistics
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()

        # The mouse pointer is hidden
        pygame.mouse.set_visible(False)

        # Clearing alien and bullet lists
        self.aliens.empty()
        self.bullets.empty()

        # Creating a new fleet and placing the ship in the center
        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Responds to keystrokes"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._close_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """Reacts to the release of keys"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creating a new projectile and including it in the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Creating an invasion fleet"""
        # Creates an alien and counts alien number in the row
        # Interval between adjacent aliens is equal to the width of the alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Determines the number of rows that fit on the screen"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creates the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Creating an alien and placing it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Reacts to the alien reaching the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Lowers the entire fleet and changes the direction of the fleet"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _change_background(self):
        """Changes background every new level (till the 20th)"""
        if self.stats.level == 1:
            self.screen.blit(self.bg1, (0, 0))
        elif self.stats.level == 2:
            self.screen.blit(self.bg2, (0, 0))
        elif self.stats.level == 3:
            self.screen.blit(self.bg3, (0, 0))
        elif self.stats.level == 4:
            self.screen.blit(self.bg4, (0, 0))
        elif self.stats.level == 5:
            self.screen.blit(self.bg5, (0, 0))
        elif self.stats.level == 6:
            self.screen.blit(self.bg6, (0, 0))
        elif self.stats.level == 7:
            self.screen.blit(self.bg7, (0, 0))
        elif self.stats.level == 8:
            self.screen.blit(self.bg8, (0, 0))
        elif self.stats.level == 9:
            self.screen.blit(self.bg9, (0, 0))
        elif self.stats.level == 10:
            self.screen.blit(self.bg10, (0, 0))
        elif self.stats.level == 11:
            self.screen.blit(self.bg11, (0, 0))
        elif self.stats.level == 12:
            self.screen.blit(self.bg12, (0, 0))
        elif self.stats.level == 13:
            self.screen.blit(self.bg13, (0, 0))
        elif self.stats.level == 14:
            self.screen.blit(self.bg14, (0, 0))
        elif self.stats.level == 15:
            self.screen.blit(self.bg15, (0, 0))
        elif self.stats.level == 16:
            self.screen.blit(self.bg16, (0, 0))
        elif self.stats.level == 17:
            self.screen.blit(self.bg17, (0, 0))
        elif self.stats.level == 18:
            self.screen.blit(self.bg18, (0, 0))
        elif self.stats.level == 19:
            self.screen.blit(self.bg19, (0, 0))
        else:
            self.screen.blit(self.bg20, (0, 0))

    def _update_screen(self):
        """Updates the images on the screen and displays a new screen"""
        self._change_background()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        # The Play button is displayed if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Displaying the last drawn screen
        pygame.display.flip()

    def _close_game(self):
        """Save high score and exit"""
        saved_high_score = self.stats.save_high_score()
        if self.stats.high_score > saved_high_score:
            with open('high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)

        sys.exit()


if __name__ == '__main__':
    # Creating an instance and launching the game
    ai = AlienInvasion()
    ai.run_game()
