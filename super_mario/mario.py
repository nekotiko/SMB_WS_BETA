
__author__ = 'bakeneko'

from utils.constants import *
from utils.sprite_loader import BricksSlider, IMAGE_SLIDER
import math
from utils import constants
from platforms import MovingPlatform
import pygame

class Mario(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """



    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image the player starts with
        # Set speed vector of player
        self.change_x = 0.0
        self.speed = 0
        self.gravity = 0
        self.__change_y = 0.0
        self.__max_vel = PY_MAX_MARIO_WALK_VEL
        self.__speed_acc = PY_MAX_WALK_ACC
        self.__running = False

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []


        # What direction is the player facing?
        self.direction = PY_RIGHT

        # List of sprites we can bump against
        self.level = None

        self.state = MARIO_STATE_NORMAL


        for index in xrange(5):
            #print index
            mario_image = IMAGE_SLIDER.get_mario('small_walk_{}'.format(index))
            self.walking_frames_r.append(mario_image)
            rotated = pygame.transform.flip(mario_image, True, False)
            self.walking_frames_l.append(rotated)

        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right

        self.rect.x += self.change_x

        pos = self.rect.x + self.level.world_shift

        if self.state == MARIO_STATE_NORMAL:
            if self.change_x:
                frame = int(pos % 30 / 10) + 1
                print(frame)
                if self.direction == PY_RIGHT:
                    self.image = self.walking_frames_r[frame]
                else:
                    self.image = self.walking_frames_l[frame]
            else:
                if self.direction == PY_RIGHT:
                    self.image = self.walking_frames_r[0]
                else:
                    self.image = self.walking_frames_l[0]

        elif self.state == MARIO_STATE_JUMPING:
            self.image = IMAGE_SLIDER.get_mario("small_jumping")

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        #we don't walk to walk outside the map.
        if self.rect.x < 0:
            self.rect.x = 0


        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0



        brick_hit_list = pygame.sprite.spritecollide(self, self.level.brick_list, False)
        for brick in brick_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = brick.rect.top
            elif self.change_y < 0:
                self.rect.top = brick.rect.bottom
                brick.bumped()

            # Stop our vertical movement
            self.change_y = 0



    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1

        else:
            seconds = self.level.physics_info['seconds']

            self.gravity += PY_JUMP_Y_FALLING_GRAVITY_1 * seconds
            if self.gravity >= PY_JUMP_Y_MAX_FALLING_ACC:
                self.gravity = PY_JUMP_Y_MAX_FALLING_RST * seconds

            self.change_y += -(PY_JUMP_X_VELOCITY_1 * seconds) + self.gravity
            if (self.change_y > PY_JUMP_Y_MAX_FALLING_ACC * seconds):
                self.change_y = PY_JUMP_Y_MAX_FALLING_RST * seconds

            print("gravity: {}".format(self.change_y))

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height
            self.change_y = 0
            self.gravity = 0

    def jump(self):
        """ Called when user hits 'jump' button. """


        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2


        if self.state == MARIO_STATE_JUMPING:
            self.change_y = -PY_JUMP_Y_HOLDING_GRAVITY_1

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = - PY_JUMP_X_VELOCITY_1 * self.level.physics_info['seconds']
            self.gravity = 0

        print("jump: {}".format(self.change_y))



    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        if self.change_x:
            self.speed += self.__speed_acc
            if self.speed > self.__max_vel:
                self.speed = self.__max_vel

        self.change_x = -(PY_MIN_MARIO_WALK_VEL + self.speed) * self.level.physics_info['seconds']
        print(self.change_x)
        self.direction = PY_LEFT

    def go_right(self):
        """ Called when the user hits the right arrow. """
        if self.change_x:
            self.speed += self.__speed_acc
            if self.speed > self.__max_vel:
                self.speed = self.__max_vel

        self.change_x = (PY_MIN_MARIO_WALK_VEL + self.speed) * self.level.physics_info['seconds']
        self.direction = PY_RIGHT

    def stop(self):
        """ Called when the user lets off the keyboard. """
        if self.change_x:
            self.speed -= self.__speed_acc
            self.change_x = (PY_MIN_MARIO_WALK_VEL + self.speed) * self.level.physics_info['seconds']
            self.change_x = self.change_x * self.direction
            if self.change_x * self.direction < 0:
                self.change_x = 0
                self.speed = 0
            #print('DEacceleration: {}'.format( self.change_x))

    #properties
    @property
    def change_y(self):
        return self.__change_y

    @change_y.setter
    def change_y(self, new_y):
        if new_y < 0: #We are jumping
            self.state = MARIO_STATE_JUMPING
        elif new_y == 0 or new_y == 1: #just touch ground
            self.state = MARIO_STATE_NORMAL

        self.__change_y = new_y

    @property
    def is_running(self):
        return self.__running

    @is_running.setter
    def is_running(self, running):
        '''
        We need to implement 10 frame deaccelearion on relase to  prevent fire
        :param running:
        :return:
        '''
        if not self.__running and running:
            print('start runnning')
            self.__max_vel = PY_MAX_MARIO_RUN_VEL
            self.__speed_acc = PY_MARIO_RUN_ACC
        elif not running and self.__running:
            print('start walking')
            self.__max_vel = PY_MAX_MARIO_WALK_VEL
            self.__speed_acc = PY_MARIO_WALK_ACC
        self.__running = running