import math

__author__ = 'bakeneko'

from pygame.math import Vector2

GAME_INFO = {'current_time': 100}

SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

SCREEN_PLAYER_OFFSET = SCREEN_WIDTH / 3 * 2 #2/3 of the screen

SIZE_ADJUSTMENT = 32
FPS = 60


SPEED = [2, 2]
BLACK = 0, 0, 0
ORIGINAL_BLOCK_SIZE = 16
SIZE_MULTIPLIER = 2
BLOCK_SIZE = ORIGINAL_BLOCK_SIZE * SIZE_MULTIPLIER
BRICK_SIZE_MULTIPLIER = 2.69
BACKGROUND_MULTIPLER = 2.679
GROUND_HEIGHT = SCREEN_HEIGHT - 62

SCORE = [0]

ANIMATION_SPEED = 130
#GRAVITY = Vector2(0.0, 1.01)
#MARIO FORCES
WALK_ACCEL = .15
RUN_ACCEL = .21
SMALL_TURNAROUND = .35

GRAVITY = 0.40
JUMP_GRAVITY = .31
JUMP_VEL = -10
FAST_JUMP_VEL = -12.5
MAX_Y_VEL = 11

MAX_RUN_SPEED = 8
MAX_WALK_SPEED = 6



MARIO_STATE_NORMAL = 0
MARIO_STATE_JUMPING = 1

#            R    G    B
GRAY         = (100, 100, 100, )
NAVYBLUE     = ( 60,  60, 100, )
WHITE        = (255, 255, 255, )
ALMOST_WHITE = (253, 253, 253, )
RED          = (255,   0,   0, )
GREEN        = (  0, 255,   0, )
FOREST_GREEN = ( 31, 162,  35, )
BLUE         = (  0,   0, 255, )
SKY_BLUE     = ( 39, 145, 251, )
YELLOW       = (255, 255,   0, )
ORANGE       = (255, 128,   0, )
PURPLE       = (255,   0, 255, )
CYAN         = (  0, 255, 255)
BLACK        = (  0,   0,   0)
NEAR_BLACK    = ( 19,  15,  48)
COMBLUE      = (233, 232, 255)
GOLD         = (255, 215,   0)
BACKGROUND_BLUE = (113, 144, 254)

MAP_QUESTION_BLOCK = (127, 51, 0)
MAP_BRICK          = (0, 74, 127)
MAP_BRICK_HOLDER    = (109, 127, 63)
MAP_SOLID_BLOCK    = (255, 200, 0)
MAP_CLOUD_1        = (87, 0, 127)
MAP_EMPTY          = (254, 254, 255)
MAP_BIG_MOUNTAIN   = (255, 233, 127)
MAP_SMALL_MOUNTAIN = (218, 255, 127)
MAP_SHORT_PIPE     = (148, 171, 91)
MAP_MID_PIPE       = (91, 127, 0)
MAP_TALL_PIPE     = (178, 0, 255)
MAP_COIN          = (255, 255, 0)
MAP_SINGLE_BUSH    =  (177, 220, 255)
MAP_DOUBLE_BUSH    = (127, 255, 142)
MAP_TRIPLE_BUSH    = (127, 0, 55)
MAP_FLAG           = (0, 255, 0)
MAP_SMALL_CASTLE   = (80, 63, 127)
MAP_GOOMBA_1       = (0, 255, 255)
MAP_TURTLE     = (127, 201, 255)

SCENARIO_BIG_HILL = 0
SCENARIO_SMALL_HILL = 1

#BRICK STATES

RESTING = 'resting'
BUMPED = 'bumped'

#COIN STATES
OPENED = 'opened'

#MUSHROOM STATES

REVEAL = 'reveal'
SLIDE = 'slide'

#COIN STATES

SPIN = 'spin'

#STAR STATES

BOUNCE = 'bounce'

#FIRE STATES

FLYING = 'flying'
BOUNCING = 'bouncing'
EXPLODING = 'exploding'

#Brick and coin box contents

MUSHROOM = 'mushroom'
STAR = 'star'
FIREFLOWER = 'fireflower'
SIXCOINS = '6coins'
COIN = 'coin'
LIFE_MUSHROOM = '1up_mushroom'

FIREBALL = 'fireball'


STAND = 'standing'
WALK = 'walk'
JUMP = 'jump'
FALL = 'fall'
SMALL_TO_BIG = 'small to big'
BIG_TO_FIRE = 'big to fire'
BIG_TO_SMALL = 'big to small'
FLAGPOLE = 'flag pole'
WALKING_TO_CASTLE = 'walking to castle'
END_OF_LEVEL_FALL = 'end of level fall'


#GOOMBA Stuff

LEFT = 'left'
RIGHT = 'right'
JUMPED_ON = 'jumped on'
DEATH_JUMP = 'death jump'

#KOOPA STUFF

SHELL_SLIDE = 'shell slide'

"""
Physics according a complete guide to SMB's Physics engine
the velocities will be expresed in /16 of the previos so
 * 16 Block
 / 1 pixel
 / 16.0 subpixel
 / 16.0 / 16.0 ss-pixel
 / 16.0 / 16.0 / 16.0 sss-pixel

 This numbers are for frame-based movement, we can do time-based movement but it will require convertion
"""
def doc_unit_to_value(num):
    if len(num) != 5:
        raise ValueError('Number can be only a String of 5 digits')

    sum = int(num[0], 16) * 16.0 + \
          int(num[1], 16) + \
          int(num[2], 16) / 16.0 + \
          int(num[3], 16) / 16.0 / 16.0 + \
          int(num[4], 16) / 16.0 / 16.0 / 16.0
    return sum * SIZE_MULTIPLIER

def doc_unit_to_pixels_per_second(num):
    pixels_per_frame = doc_unit_to_value(num)
    return pixels_per_frame * FPS

PY_RIGHT = 1
PY_LEFT  = -1

PY_MAX_MARIO_WALK_VEL = doc_unit_to_pixels_per_second('01900')
PY_MIN_MARIO_WALK_VEL = doc_unit_to_pixels_per_second('00130')
PY_MARIO_WALK_ACC     = doc_unit_to_pixels_per_second('00098')
PY_MARIO_WALK_DEC     = doc_unit_to_pixels_per_second('000D0')
PY_MAX_MARIO_RUN_VEL  = doc_unit_to_pixels_per_second('02900')
PY_MARIO_RUN_ACC  = doc_unit_to_pixels_per_second('000E4')

PY_JUMP_X_VELOCITY_1 = doc_unit_to_pixels_per_second('01000')
PY_JUMP_X_VELOCITY_2 = doc_unit_to_pixels_per_second('024FF')
PY_JUMP_X_VELOCITY_3 = doc_unit_to_pixels_per_second('02500')

PY_JUMP_Y_VELOCITY_1 = doc_unit_to_pixels_per_second('04000')
PY_JUMP_Y_VELOCITY_2 = doc_unit_to_pixels_per_second('04000')
PY_JUMP_Y_VELOCITY_3 = doc_unit_to_pixels_per_second('05000')

PY_JUMP_Y_HOLDING_GRAVITY_1 = doc_unit_to_pixels_per_second('00180')
PY_JUMP_Y_HOLDING_GRAVITY_2 = doc_unit_to_pixels_per_second('00220')
PY_JUMP_Y_HOLDING_GRAVITY_3 = doc_unit_to_pixels_per_second('00220')

PY_JUMP_Y_FALLING_GRAVITY_1 = doc_unit_to_pixels_per_second('00440')
PY_JUMP_Y_FALLING_GRAVITY_2 = doc_unit_to_pixels_per_second('003E0')
PY_JUMP_Y_FALLING_GRAVITY_3 = doc_unit_to_pixels_per_second('005D0')

PY_JUMP_Y_MAX_FALLING_ACC = doc_unit_to_pixels_per_second('04800')
PY_JUMP_Y_MAX_FALLING_RST = doc_unit_to_pixels_per_second('04000')

##Deduced PY
PY_MAX_WALK_ACC = PY_MAX_MARIO_WALK_VEL - PY_MIN_MARIO_WALK_VEL