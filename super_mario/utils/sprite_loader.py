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

        'question_mark_0': (384, 0, 16, 16),
        'question_mark_1': (400, 0, 16, 16),
        'question_mark_2': (416, 0, 16, 16),
        'question_mark_3': (432, 0, 16, 16),#empty

        'mario_small_walk_0' : (178, 32, 12, 16),
        'mario_small_walk_1' : (80, 32, 14, 16),
        'mario_small_walk_2' : (98, 32, 12, 16),
        'mario_small_walk_3' : (114, 32, 12, 16),
        'mario_small_walk_4' : (128, 32, 14, 16),
        'mario_small_jumping': (144, 32, 16, 16),
        'mario_dying': (160, 32, 16, 16),

        'goomba_1': (0, 16, 16, 16),
        'goomba_2': (16,16, 16, 16),
        'goomba_3': (32,16, 16, 16),

        'turtle_1': (96, 8, 16, 24),
        'turtle_2': (112,8, 16, 24),
        'turtle_3': (160,16, 16, 16),

        'cloud_1':    (0,320,45,24),

        'mountain_0': (128,128,16,16),
        'mountain_1': (128,144,16,16),
        'mountain_2': (144,128,16,16),
        'mountain_3': (144,144,16,16),
        'mountain_4': (160,128,16,16),
        'mountain_5': (160,144,16,16),

        'pipe_top': (1, 129, 30, 14),
        'pipe_body': (3, 144, 26, 15),

        'bush_0': (176, 144, 16, 16),
        'bush_1': (192, 144, 16, 16),
        'bush_2': (208, 144, 16, 16),

        'castle_0': (176, 0, 16, 16),
        'castle_1': (176, 16, 16, 16),
        'castle_2': (192, 0, 16, 16),
        'castle_3': (192, 16, 16, 16),
        'castle_4': (208, 16, 16, 16),
        'castle_5': (208, 0, 16, 16),
        'castle_6': (224, 0, 16, 16),

}




class ImageSlider(object):

    def __init__(self):

        print "BrickSlider Inited"
        self.images = {}

    def get_mario(self, name):
        return self._get_image('mario_' + name, '../assets/mario_bros.png', 'mario')

    def get_image(self, name, multiplier=SIZE_MULTIPLIER):
        return self._get_image(name, '../assets/tile_set.png', 'asset', multiplier)


    def get_enemies(self, name):
        image = self._get_image(name, '../assets/enemies.png', 'enemies')
        return image

    def _get_image(self, name, path, type, multiplier=SIZE_MULTIPLIER):
        image = self.images.get(name)
        if not image:
            image = self._cut_image(name, path, type, multiplier)
            self.images[name] = image

        return image

    def _cut_image(self, name, path, type, multiplier=SIZE_MULTIPLIER):
        global TILE_IMAGE
        global MARIO_IMAGES
        global ENEMY_IMAGES


        if not TILE_IMAGE and type == 'asset':
            TILE_IMAGE = self.convert(pg.image.load(path))

        if not MARIO_IMAGES and type == 'mario':
            MARIO_IMAGES = self.convert(pg.image.load(path))

        if not ENEMY_IMAGES and type == 'enemies':
            ENEMY_IMAGES = self.convert(pg.image.load(path))

        IMAGE = TILE_IMAGE
        if type == 'mario':
            IMAGE = MARIO_IMAGES
        elif type == 'enemies':
            IMAGE = ENEMY_IMAGES

        dimensions = BRICK_DIMENTION[name]
        width, height = dimensions[2:4]

        # Create a new blank image, the SRCALPHA will keep the Alpha information form the orginal PNG
        image = pg.Surface([width, height], pg.SRCALPHA, 32)

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(IMAGE, (0, 0), dimensions)
        scale_image = pg.transform.scale(image,
                                         (int(width * multiplier),
                                          int(height * multiplier)))
        return scale_image


    def convert(self, image):
        if image.get_alpha():
            img = image.convert_alpha()
            return img
        else:
            img = image.convert()
            return img




IMAGE_SLIDER = ImageSlider()

##Composite Images

def get_bush(size=1):
    images = []
    for x in xrange(3):
        images.append(IMAGE_SLIDER.get_image('bush_{}'.format(x)))

    height = BLOCK_SIZE
    #2 is the head and tail of the bush
    parts = 2 + size
    width = BLOCK_SIZE * parts

    bush = pg.Surface([width, height], pg.SRCALPHA, 32)

    bush.blit(images[0], (0, 0))
    for x in xrange(BLOCK_SIZE, BLOCK_SIZE * size + 1 , BLOCK_SIZE ):
        bush.blit(images[1], (x ,0))

    bush.blit(images[2], (width - BLOCK_SIZE ,0))

    return bush


def get_pipe(size=1):
    top = IMAGE_SLIDER.get_image('pipe_top')
    body = IMAGE_SLIDER.get_image('pipe_body')
    b_height = body.get_height()

    height = top.get_height() + (b_height * size)
    width = top.get_width()

    new_pipe = pg.Surface([width, height], pg.SRCALPHA, 32)

    new_pipe.blit(top, (0, 0))
    for y in xrange(top.get_height(), b_height * size + 1, b_height):
        new_pipe.blit(body, (4, y))

    return new_pipe

def get_castle():
    width = BLOCK_SIZE * 5
    height = BLOCK_SIZE * 5
    images = []

    for index in xrange(7):
        images.append(IMAGE_SLIDER.get_image('castle_{}'.format(index)))

    map = [(-1, 0, 0, 0, -1),
           (-1, 2, 5, 6, -1),
           (0, 1, 1, 1, 0),
           (5, 5, 3, 5, 5),
           (5, 5, 4, 5, 5),]

    castle = pg.Surface([width, height], pg.SRCALPHA, 32)

    i = j = 0
    for x in xrange(0, width, BLOCK_SIZE):
        for y in xrange(0, height, BLOCK_SIZE):
            index = map[j][i]
            if index >= 0:
                block  = images[index]
                castle.blit(block, (x, y))
            j += 1
        i += 1
        j = 0

    return castle

def get_hill(size):
    '''
    big_hill, 5 w x 3h
    :param size:
    :return:
    '''

    if size == SCENARIO_BIG_HILL:
        width = 5 * BLOCK_SIZE
        height = 3 * BLOCK_SIZE

        hill_map = [(-1, -1, 2, -1, -1),
                    (-1, 0, 1, 4, -1),
                    ( 0, 1, 3, 5, 4)]
    elif size == SCENARIO_SMALL_HILL:
        width = 3 * BLOCK_SIZE
        height = 2 * BLOCK_SIZE

        hill_map = [(-1, 2, -1),
                    (0, 1, 4)]

    images = []

    for index in xrange(6):
        images.append(IMAGE_SLIDER.get_image('mountain_{}'.format(index)))

    hill = pg.Surface([width, height], pg.SRCALPHA, 32)

    i = j = 0
    for x in xrange(0, width, BLOCK_SIZE):
        for y in xrange(0, height, BLOCK_SIZE):
            index = hill_map[j][i]
            if index >= 0:
                block  = images[index]
                hill.blit(block, (x, y))
            j += 1
        i += 1
        j = 0

    return hill
