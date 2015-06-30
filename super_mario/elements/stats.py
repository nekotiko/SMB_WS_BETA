import pygame
from utils.constants import WHITE
from utils.constants import BLOCK_SIZE
from utils.loader import get_font

__author__ = 'bakeneko'


class Stats(object):

    def __init__(self, time=400):
        self.font = get_font(16)
        self.world = ' 1-1 '
        self.worltime  = 0
        self.lives = 3
        self.score = 0
        self.coins = 0
        self.time = 400


    def set_level_time(self, time):
        self.time = time

    def render_stats(self, screen, level):

        self.time -= level.physics_info['seconds']

        ren = self.font.render("MARIO", 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE, 16))

        ren = self.font.render("{:06}".format(self.score), 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE, 33))

        ren = self.font.render("x {:02}".format(self.coins), 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE * 7, 33))

        ren = self.font.render("WORLD", 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE * 11, 16))

        ren = self.font.render(self.world, 1, (255, 255, 255))
        screen.blit(ren, (BLOCK_SIZE * 11, 33))

        ren1 = self.font.render("TIME".format(self.time), 1, (255, 255, 255))
        screen.blit(ren1, (BLOCK_SIZE * 16, 16))

        ren2 = self.font.render(" {:03}".format(int(self.time)), 1, WHITE)
        screen.blit(ren2, (BLOCK_SIZE * 16, 33))


