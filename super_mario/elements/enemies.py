from utils.sprite_loader import IMAGE_SLIDER

__author__ = 'bakeneko'

import pygame as pg
import utils.constants as c

class Enemy(pg.sprite.Sprite):
    """Base class for all enemies (Goombas, Koopas, etc.)"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)


    def setup_enemy(self, x, y, level, direction, name, setup_frames):
        """Sets up various values for enemy"""
        #self.sprite_sheet = setup.GFX['smb_enemies_sheet']
        self.frames = []
        self.frame_index = 0
        self.animate_timer = 0
        self.death_timer = 0
        self.gravity = 1.5
        self.state = c.WALK
        self.level = level

        self.name = name
        self.direction = direction
        setup_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.set_velocity()
        self.current_time = 0


    def set_velocity(self):
        """Sets velocity vector based on direction"""
        if self.direction == c.LEFT:
            self.x_vel = -2
        else:
            self.x_vel = 2

        self.y_vel = 0


    def handle_state(self):
        """Enemy behavior based on state"""
        if self.state == c.WALK:
            self.walking()
        elif self.state == c.FALL:
            self.falling()
        elif self.state == c.JUMPED_ON:
            self.jumped_on()
        elif self.state == c.SHELL_SLIDE:
            self.shell_sliding()
        elif self.state == c.DEATH_JUMP:
            self.death_jumping()


    def walking(self):
        """Default state of moving sideways"""
        if (self.current_time - self.animate_timer) > 125:
            if self.frame_index == 0:
                self.frame_index += 1
            elif self.frame_index == 1:
                self.frame_index = 0

            self.animate_timer = self.current_time

        block_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.x_vel > 0:
                self.rect.right = block.rect.left
                self.direction = c.LEFT
            elif self.x_vel < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.direction = c.RIGHT

            self.set_velocity()


    def falling(self):
        """For when it falls off a ledge"""
        if self.y_vel < 10:
            self.y_vel += self.gravity


    def jumped_on(self):
        """Placeholder for when the enemy is stomped on"""
        pass


    def death_jumping(self):
        """Death animation"""
        self.rect.y += self.y_vel
        self.rect.x += self.x_vel
        self.y_vel += self.gravity

        if self.rect.y > 600:
            self.kill()


    def start_death_jump(self, direction):
        """Transitions enemy into a DEATH JUMP state"""
        self.y_vel = -8
        if direction == c.RIGHT:
            self.x_vel = 2
        else:
            self.x_vel = -2
        self.gravity = .5
        self.frame_index = 3
        self.image = self.frames[self.frame_index]
        self.state = c.DEATH_JUMP


    def animation(self):
        """Basic animation, switching between two frames"""
        self.image = self.frames[self.frame_index]


    def update(self):
        """Updates enemy behavior"""
        self.current_time = pg.time.get_ticks()
        self.handle_state()
        self.animation()




class Goomba(Enemy):

    def __init__(self,x=0, y=c.GROUND_HEIGHT, level=None, direction=c.LEFT, name='goomba'):
        Enemy.__init__(self)
        self.setup_enemy(x, y, level, direction, name, self.setup_frames)
        self.setup_frames()


    def setup_frames(self):
        """Put the image frames in a list to be animated"""

        self.frames.append(
            IMAGE_SLIDER.get_enemies('goomba_1'))
        self.frames.append(
            IMAGE_SLIDER.get_enemies('goomba_2'))

        self.frames.append(pg.transform.flip(self.frames[0], False, True))


    def jumped_on(self):
        """When Mario squishes him"""
        self.frame_index = 2

        if (self.current_time - self.death_timer) > 500:
            self.kill()



class Turtle(Enemy):

    def __init__(self,x=0, y=c.GROUND_HEIGHT, level=None, direction=c.LEFT, name='Turtle'):
        Enemy.__init__(self)
        self.setup_enemy(x, y-16, level, direction, name, self.setup_frames)
        self.setup_frames()


    def setup_frames(self):
        """Put the image frames in a list to be animated"""

        self.frames.append(
            IMAGE_SLIDER.get_enemies('turtle_1'))
        self.frames.append(
            IMAGE_SLIDER.get_enemies('turtle_2'))

        self.frames.append(pg.transform.flip(self.frames[0], False, True))


    def jumped_on(self):
        """When Mario squishes him"""
        self.frame_index = 2

        if (self.current_time - self.death_timer) > 500:
            self.kill()

