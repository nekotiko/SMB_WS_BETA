import pygame
from utils.constants import WHITE
from utils.constants import BLOCK_SIZE
from utils.loader import get_font
from super_mario.utils.sprite_loader import IMAGE_SLIDER

__author__ = 'bakeneko'


class Stats(object):

    def __init__(self, level, time=400 ):
        self.font = get_font(16)
        self.world = ' 1-1 '
        self.worltime  = 0
        self.lives = 3
        self.score = 0
        self.coins = 0
        self.time = 400
        self.coin = ScoreCoin(BLOCK_SIZE * 6, 33)
        self.x = IMAGE_SLIDER.get_item('score_x', 1.5)

    def set_level_time(self, time):
        self.time = time

    def render_stats(self, screen, level):

        self.time -= level.physics_info['seconds']



        ren = self.font.render("MARIO", 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE, 16))

        ren = self.font.render("{:06}".format(self.score), 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE, 33))


        self.coin.update()
        screen.blit(self.coin.image, (BLOCK_SIZE * 6, 33))
        screen.blit(self.x, (BLOCK_SIZE * 6.5, 33))

        ren = self.font.render("{:02}".format(self.coins), 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE * 7, 33))

        ren = self.font.render("WORLD", 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE * 11, 16))

        ren = self.font.render(self.world, 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE * 11, 33))

        ren1 = self.font.render("TIME".format(self.time), 1, (255, 255, 255))
        screen.blit(ren1, (BLOCK_SIZE * 16, 16))

        ren2 = self.font.render(" {:03}".format(int(self.time)), 1, WHITE)
        screen.blit(ren2, (BLOCK_SIZE * 16, 33))


class ScoreCoin(object):

    def __init__(self, x, y):

        self.frames = []
        self.frame_index = 0
        for index in xrange(0, 3):
            self.frames.append(IMAGE_SLIDER.get_item('score_coin_{}'.format(index), 1.5))

        self.frames.append(self.frames[1])
        self.frames.append(self.frames[0])
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_count = 0


    def update(self):
        self.frame_count += 1
        if self.frame_count == 20:
            self.frame_count = 0
            self.image = self.frames[self.frame_index]
            self.frame_index += 1
            if self.frame_index == 5:
                self.frame_index = 0
