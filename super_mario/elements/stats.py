import pygame
from utils.constants import WHITE
from super_mario.utils.constants import BLOCK_SIZE

__author__ = 'bakeneko'

"""
 def draw_stats(self):
        for i in range(1):
            self.screen.blit(self.heart2, (16 + i*34, 16))
        for i in range(self.player.hp):
            self.screen.blit(self.heart1, (16 + i*34, 16))
        self.screen.blit(self.heroimg, (313, 16))
        self.screen.blit(self.heroimg2, (235, 10))
        lives = self.lives
        if lives < 0:
            lives = 0
        ren = self.font.render("Mario", 1, (255, 255, 255))
        self.screen.blit(ren, (132-ren.get_width(), 16))
        ren = self.font.render("Score%06d" % self.score, 1, (255, 255, 255))
        self.screen.blit(ren, (228-ren.get_width(), 33))
        ren = self.font.render("x%d" % lives, 1, (255, 255, 255))
        self.screen.blit(ren, (315+34, 24))
        ren = self.font.render("x%02d" % self.coin, 1, (255, 255, 255))
        self.screen.blit(ren, (300-ren.get_width(), 16))
        ren = self.font.render("FPS    %d" % self.clock.get_fps(), 1, (255, 255, 255))
        self.screen.blit(ren, (451, 16))
        ren1 = self.font.render("Time: %d" % self.time, 1, (255, 255, 255))
        ren2 = self.font.render("Time: %d" % self.time, 1, Color("#ffffff"))
        self.screen.blit(ren1, (450, 35))
        self.screen.blit(ren2, (450, 35))
        if self.time <= 100:
            ren = self.font.render("GOTTA GO FAST", 1, (255, 255, 255))
            self.screen.blit(ren, (630-ren.get_width(), 60))
"""


class Stats(object):

    def __init__(self, time=400):
        self.font = pygame.font.Font('../assets/font/font.ttf', 16)
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


