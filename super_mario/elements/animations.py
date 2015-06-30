from utils.loader import play_sound
from utils.loader import get_font

__author__ = 'bakeneko'


import pygame
from utils.sprite_loader import IMAGE_SLIDER
from utils.constants import *

class DyingMario(pygame.sprite.Sprite):

    def __init__(self, x, y, level):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image the player starts with
        # Set speed vector of player
        self.image = IMAGE_SLIDER.get_mario('dying')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
        self.change_y = -PY_JUMP_Y_VELOCITY_1 * self.level.physics_info['seconds']
        self.gravity = 0


    def update(self):
        seconds = self.level.physics_info['seconds']
        self.gravity += PY_JUMP_Y_HOLDING_GRAVITY_1 * seconds
        self.change_y = (-PY_JUMP_Y_VELOCITY_1 * seconds) + self.gravity
        self.rect.y += self.change_y
        if self.rect.y >= SCREEN_HEIGHT + self.rect.height:
            self.kill()



class Points(pygame.sprite.Sprite):

    font = None

    def __init__(self, score, x, y, level):

        pygame.sprite.Sprite.__init__(self)
        if not Points.font:
            Points.font = get_font(8)
        self.timeout = 1
        self.level = level
        self.image = Points.font.render(str(score), False, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        seconds = self.level.physics_info['seconds']
        self.rect.y += -10 * seconds
        self.timeout -= seconds
        if self.timeout <= 0:
            self.kill()

