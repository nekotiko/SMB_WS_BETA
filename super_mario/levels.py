
__author__ = 'bakeneko'

import pygame

from elements.stats import Stats
from utils import constants

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """



    def __init__(self, player):

         # Lists of sprites used in all levels. Add or remove
        # lists as needed for your game. """
        self.platform_list = None
        self.enemy_list = None
        self.brick_list = None
        self.scenario_list = None
        self.physics_info = {'play_time': 0, 'seconds': 0, 'current_time': 0}
        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000
        self.stats = Stats(400)


        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list  = pygame.sprite.Group()
        self.enemy_list     = pygame.sprite.Group()
        self.brick_list     = pygame.sprite.Group()
        self.scenario_list  = pygame.sprite.Group()
        #Animations are elements that interact with nothing and will be removed soon
        self.animation_list  = pygame.sprite.Group()
        self.player = player


    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.animation_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(constants.BACKGROUND_BLUE,  None)


        # Draw all the sprite lists that we have
        self.scenario_list.draw(screen)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.animation_list.draw(screen)
        self.stats.render_stats(screen, self)



    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x


        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for scenario in self.scenario_list:
            scenario.rect.x += shift_x

    def add_platform(self, platform):
        self.platform_list.add(platform)

    def add_brick(self, brick):
        self.brick_list.add(brick)
        self.add_platform(brick)

    def add_enemy(self, enemy):
        self.enemy_list.add(enemy)

    def add_scenario(self, scenario):
        self.scenario_list.add(scenario)

    def add_animation(self, animation):
        self.animation_list.add(animation)

    def add_point(self, points):
        self.stats.score += points