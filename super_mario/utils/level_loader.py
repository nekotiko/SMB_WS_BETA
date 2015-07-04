import pygame
from constants import *
from elements.bricks import BrickPlatform, QuestionBox, Brick, SolidPlatform, Pipe
from elements.enemies import Goomba, Turtle
from elements.scenario import ScenarioItem
from elements.scenario import Hill
from utils.sprite_loader import get_bush, get_castle
from elements.scenario import ScenarioItemWithImage, ScenarioCastle
from super_mario.elements.scenario import Pole
from super_mario.utils.sprite_loader import get_pole

__author__ = 'bakeneko'




def load_level(level_instance, lvl=1):
        level = pygame.image.load("../assets/levels/lvl{}.png".format(lvl)).convert()
        x = 0
        y = 0
        for y in xrange(level.get_height()):
            y = y
            for x in xrange(level.get_width()):
                x = x
                a_x = x * SIZE_ADJUSTMENT
                a_y = y * SIZE_ADJUSTMENT
                color = level.get_at((x, y))
                if compare_with_depth(color, BLACK):
                    level_instance.add_platform(BrickPlatform(a_x, a_y))

                elif compare_with_depth(color, MAP_QUESTION_BLOCK):
                    level_instance.add_brick(QuestionBox(a_x, a_y, level_instance))

                elif compare_with_depth(color, MAP_BRICK):
                    level_instance.add_brick(Brick(a_x, a_y))

                elif compare_with_depth(color, MAP_BRICK_HOLDER):
                    level_instance.add_brick(Brick(a_x, a_y,))

                elif compare_with_depth(color, MAP_SOLID_BLOCK):
                    level_instance.add_platform(SolidPlatform(a_x, a_y))

                elif compare_with_depth(color, MAP_CLOUD_1):
                    level_instance.add_scenario(ScenarioItem(a_x, a_y, 'cloud_1'))

                elif compare_with_depth(color, MAP_BIG_MOUNTAIN):
                    level_instance.add_scenario(Hill(a_x, a_y, SCENARIO_BIG_HILL))


                elif compare_with_depth(color, MAP_SMALL_MOUNTAIN):
                    level_instance.add_scenario(Hill(a_x, a_y, SCENARIO_SMALL_HILL))
                    #level_instance.add_scenario(Pole(a_x, a_y))

                elif compare_with_depth(color, MAP_SHORT_PIPE):
                    level_instance.add_platform(Pipe(a_x, a_y))

                elif compare_with_depth(color, MAP_MID_PIPE):
                    level_instance.add_platform(Pipe(a_x, a_y, 2))

                elif compare_with_depth(color, MAP_TALL_PIPE):
                    level_instance.add_platform(Pipe(a_x, a_y, 3))

                elif  compare_with_depth(color, MAP_SINGLE_BUSH):
                    level_instance.add_scenario(ScenarioItemWithImage(a_x, a_y, get_bush(1)))

                elif  compare_with_depth(color, MAP_DOUBLE_BUSH):
                    level_instance.add_scenario(ScenarioItemWithImage(a_x, a_y, get_bush(2)))

                elif  compare_with_depth(color, MAP_TRIPLE_BUSH):
                    level_instance.add_scenario(ScenarioItemWithImage(a_x, a_y, get_bush(3)))

                elif  compare_with_depth(color, MAP_SMALL_CASTLE):
                    level_instance.add_scenario(ScenarioCastle(a_x, a_y, get_castle()))


                elif  compare_with_depth(color, MAP_GOOMBA_1):
                    level_instance.add_enemy(Goomba(a_x, a_y, level_instance))

                elif  compare_with_depth(color, MAP_TURTLE):
                    level_instance.add_enemy(Turtle(a_x, a_y, level_instance))

                elif  compare_with_depth(color, MAP_FLAG):
                    level_instance.add_scenario(Pole(a_x, a_y))

                elif compare_with_depth(color, MAP_COIN):

                    pass
                else:
                    if not compare_with_depth(color, MAP_EMPTY):
                        print("Missing element for color {}".format(color))




def compare_with_depth(depth_color, color, depth=(255,)):
    return depth_color == color[0:3] + depth
