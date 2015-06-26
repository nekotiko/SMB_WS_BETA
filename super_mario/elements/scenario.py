from utils.constants import BLACK
from utils.sprite_loader import IMAGE_SLIDER

__author__ = 'bakeneko'


__author__ = 'bakeneko'

import pygame as pg
#from .. import setup
from utils import constants as c
#from . import powerups
#from . import coin


class ScenarioItem(pg.sprite.Sprite):

    def __init__(self, x, y, image ):
        pg.sprite.Sprite.__init__(self)
        self.image = IMAGE_SLIDER.get_image(image,color_key=BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)
