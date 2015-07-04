from utils.sprite_loader import get_hill
from super_mario.utils.sprite_loader import get_pole
from utils.constants import SCENARIO_BIG_HILL, BLOCK_SIZE

__author__ = 'bakeneko'

import pygame as pg
from utils.sprite_loader import IMAGE_SLIDER


class ScenarioItem(pg.sprite.Sprite):

    def __init__(self, x, y, image ):
        pg.sprite.Sprite.__init__(self)
        self.image = IMAGE_SLIDER.get_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class ScenarioItemWithImage(pg.sprite.Sprite):

    def __init__(self, x, y, image ):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(bottomleft=(x-32,y))
        self.rect.y = y

class ScenarioCastle(pg.sprite.Sprite):

    def __init__(self, x, y, image ):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(bottomleft=(x+32,y+32))


class Hill(pg.sprite.Sprite):

    def __init__(self, x, y, size=SCENARIO_BIG_HILL):
        pg.sprite.Sprite.__init__(self)
        self.image = get_hill(size)
        self.rect = self.image.get_rect(bottomleft=(x, y+ 32))


class Pole(pg.sprite.Sprite):
    def __init__(self, x, y, size=SCENARIO_BIG_HILL):
        pg.sprite.Sprite.__init__(self)
        self.image = get_pole()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - BLOCK_SIZE * 9
