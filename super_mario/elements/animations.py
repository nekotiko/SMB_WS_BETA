from utils.loader import play_sound
from utils.loader import get_font

__author__ = 'bakeneko'


import pygame
from utils.sprite_loader import IMAGE_SLIDER
from super_mario.utils.constants import *

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



class CollectedCoin(pygame.sprite.Sprite):

    def __init__(self, x, y, level):

        pygame.sprite.Sprite.__init__(self)

        self.frame_index = 0
        self.frames = []
        self.level = level
        for index in xrange(0, 4):
            self.frames.append(IMAGE_SLIDER.get_item('collected_coin_{}'.format(index), 1))

        self.image = self.frames[self.frame_index]
        self.rect = self.frames[1].get_rect() #1 is the wider coin
        self.rect.x = x
        self.rect.y = y

        self.timeout = 1
        self.gravity = 0

        self.frame_count = 0
        self.level.stats.coins += 1

    def update(self):
        if self.timeout < 0: return
        seconds = self.level.physics_info['seconds']
        self.frame_count += 1

        if self.frame_count == 2:
            self.frame_count = 0
            self.frame_index += 1
            if self.frame_index == 4:
                self.frame_index = 0

        self.image = self.frames[self.frame_index]

        #if self.frame_index == 0:
        self.gravity += (PY_JUMP_Y_HOLDING_GRAVITY_1 * seconds)
        self.rect.y += (-PY_JUMP_Y_VELOCITY_1 * seconds) + self.gravity
        self.timeout -= seconds
            #print(self.frame_index)

        if self.timeout <= 0:
            point = Points(200, self.rect.x, self.rect.y, self.level)
            self.level.add_animation(point)
            self.kill()

