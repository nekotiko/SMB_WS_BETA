__author__ = 'bakeneko'

import pygame as pg
from constants import *


MARIO_SPRITE_INIT = 80
MARIO_SPRITE_WITDH = 32
MARIO_SPRITE_GAP = 2


#part_6
TILE_IMAGE = None
MARIO_IMAGES = None
ENEMY_IMAGES = None



#x,y, width, height
BRICK_DIMENTION = {
        'red_floor': (0, 0, 16, 16),
        'red_brick': (16, 0, 16, 16),
        'empty_brick': (432, 0, 16, 16),
        'broken_brick': (68, 20, 8, 8),
        'solid_brick': (0, 16, 16, 16),

        'question_mark_1': (384, 0, 16, 16),
        'question_mark_2': (400, 0, 16, 16),
        'question_mark_3': (416, 0, 16, 16),
        'question_mark_4': (432, 0, 16, 16),#empty

        'mario_small_walk_0' : (178, 32, 12, 16),
        'mario_small_walk_1' : (80, 32, 14, 16),
        'mario_small_walk_2' : (98, 32, 12, 16),
        'mario_small_walk_3' : (114, 32, 12, 16),
        'mario_small_walk_4' : (128, 32, 14, 16),
        'mario_small_jumping': (144, 32, 16, 16),

        'goomba_1': (0, 16, 16, 16),
        'goomba_2': (16,16, 16, 16),
        'goomba_3': (32,16, 16, 16),

        'cloud_1':    (0,320,45,22),
        'mountain_1': (127,127,48, 32),

        'pipe_top': (1, 129, 30, 14),
        'pipe_body': (3, 144, 26, 15),

}




class BricksSlider(object):

    def __init__(self):

        print "BrickSlider Inited"
        self.images = {}

    def get_mario(self, name):
        return self._get_image('mario_' + name, '../assets/mario_bros.png', 'mario', color_key=BLACK)

    def get_image(self, name, multiplier=SIZE_MULTIPLIER, color_key=WHITE):
        return self._get_image(name, '../assets/tile_set.png', 'asset', multiplier, color_key)


    def get_enemies(self, name, color_key=BLACK):
        image = self._get_image(name, '../assets/enemies.png', 'enemies', color_key=color_key)
        print("Enemy Backgound {}".format(image.get_at((0,0))))
        return image

    def _get_image(self, name, path, type, multiplier=SIZE_MULTIPLIER, color_key=WHITE):
        image = self.images.get(name)
        if not image:
            image = self._cut_image(name, path, type, color_key, multiplier)
            self.images[name] = image

        return image


    def get_pipe(self, size=1):
        top = self.get_image('pipe_top')
        body = self.get_image('pipe_body')
        b_height = body.get_height()

        height = top.get_height() + (b_height * size)
        width = top.get_width()

        new_pipe = pg.Surface([width, height]).convert()
        new_pipe.fill(WHITE)
        new_pipe.set_colorkey(WHITE)
        new_pipe.blit(top, (0, 0))
        for y in xrange(top.get_height(), b_height * size + 1, b_height):
            new_pipe.blit(body, (4, y))

        return new_pipe





    def _cut_image(self, name, path, type, color_key, multiplier=SIZE_MULTIPLIER):
        global TILE_IMAGE
        global MARIO_IMAGES
        global ENEMY_IMAGES


        if not TILE_IMAGE and type == 'asset':
            TILE_IMAGE = self.convert(pg.image.load(path), color_key)

        if not MARIO_IMAGES and type == 'mario':
            MARIO_IMAGES = self.convert(pg.image.load(path), color_key)

        if not ENEMY_IMAGES and type == 'enemies':
            ENEMY_IMAGES = self.convert(pg.image.load(path), color_key)

        IMAGE = TILE_IMAGE
        if type == 'mario':
            IMAGE = MARIO_IMAGES
        elif type == 'enemies':
            IMAGE = ENEMY_IMAGES

        dimensions = BRICK_DIMENTION[name]
        width, height = dimensions[2:4]

        # Create a new blank image
        image = pg.Surface([width, height])
        #image.set_alpha(IMAGE.get_alpha())
        image.set_colorkey(color_key)

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(IMAGE, (0, 0), dimensions)

        scale_image = pg.transform.scale(image,
                                         (int(width * multiplier),
                                          int(height * multiplier)))
        return scale_image

    def convert(self, image, color_key):
        if image.get_alpha():
            img = image.convert_alpha()
            img.set_colorkey(WHITE)
            return img
        else:
            img = image.convert()
            img.set_colorkey(BLACK)
            return img




IMAGE_SLIDER = BricksSlider()


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pg.image.load(file_name).convert()


    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pg.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)

        # Return the image
        return image