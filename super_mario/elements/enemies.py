from utils.loader import play_sound

__author__ = 'bakeneko'

import pygame as pg
import utils.constants as c
from utils.sprite_loader import IMAGE_SLIDER




class Enemy(pg.sprite.Sprite):

    count = 0

    """Base class for all enemies (Goombas, Koopas, etc.)"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)


    def setup_enemy(self, x, y, level, direction, name, setup_frames):
        """Sets up various values for enemy"""
        #self.sprite_sheet = setup.GFX['smb_enemies_sheet']
        self.frames = []
        self.frame_index = 0

        self.gravity = 4.5
        self.state = c.WALK
        self.level = level

        self.name = name + str(Enemy.count)
        Enemy.count += 1
        self.direction = direction
        self.image_direction = direction
        setup_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.current_time = 0
        self.set_velocity()


    def set_velocity(self):
        """Sets velocity vector based on direction"""
        if self.direction == c.LEFT:
            self.x_vel = -1
        else:
            self.x_vel =  1

        #let's flip the direction
        if self.direction != self.image_direction:
            self.image_direction = self.direction
            for index, image in enumerate(self.frames):
                self.frames[index] = pg.transform.flip(image, True, False)

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

        self.calc_grav()

        """Default state of moving sideways"""
        #print("Wlaking : {}".format(self.current_time - self.animate_timer))
        if self.current_time  > 0.25:
            if self.frame_index == 0:
                self.frame_index += 1
            elif self.frame_index == 1:
                self.frame_index = 0

            self.current_time = 0


        self.rect.x += self.x_vel

        block_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        enemy_hit_list = pg.sprite.spritecollide(self, self.level.enemy_list, False)
        try:
            enemy_hit_list.remove(self)
        except ValueError: #The is nothing to do we don't exist anymore
            pass

        block_hit_list.extend(enemy_hit_list)

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


        #move up and down.

        self.rect.y += self.y_vel

        block_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        # Check if it is falling
        for block in block_hit_list:
        # Reset our position based on the top/bottom of the object.
            if self.y_vel > 0:
                self.rect.bottom = block.rect.top
            elif self.y_vel < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.y_vel = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.y_vel == 0:
            if self.y_vel < 150:
                self.y_vel += self.gravity

         # See if we are on the ground.
        if self.rect.y >= c.SCREEN_HEIGHT + self.rect.height  and self.y_vel >= 0:
            self.kill()



    def falling(self):
        """For when it falls off a ledge"""
        if self.y_vel < 10:
            self.y_vel += self.gravity


    def jumped_on(self):
        """Placeholder for when the enemy is stomped on"""
        pass


    def start_death_jump(self, direction):
        print("DEATH JUMP")
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
        #We only want enemies to move when we are close
        pos = abs(self.level.world_shift - c.SCREEN_WIDTH)

        if self.rect.x <= pos:
            self.current_time += self.level.physics_info['seconds']
            self.handle_state()
            self.animation()
            if self.rect.x <= - c.BLOCK_SIZE * 5: #Too far behind let's get rid of it
                self.kill()



class Goomba(Enemy):

    def __init__(self,x=0, y=c.GROUND_HEIGHT, level=None, direction=c.LEFT, name='goomba'):
        Enemy.__init__(self)
        self.setup_enemy(x, y, level, direction, name, self.setup_frames)



    def setup_frames(self):
        """Put the image frames in a list to be animated"""

        self.frames.append(
            IMAGE_SLIDER.get_enemies('goomba_1'))
        self.frames.append(
            IMAGE_SLIDER.get_enemies('goomba_2'))
        self.frames.append(
            IMAGE_SLIDER.get_enemies('goomba_3'))

        self.frames.append(pg.transform.flip(self.frames[0], False, True))


    def jumped_on(self):
        """When Mario squishes him"""
        if (self.state != c.JUMPED_ON):
            self.level.add_point(100, self.rect)
            play_sound(c.SND_STOMP)
        self.state = c.JUMPED_ON
        self.frame_index = 2
        self.x_vel = 0

        if self.current_time > 0.50: #half second
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

        self.frames.append(IMAGE_SLIDER.get_enemies('turtle_3'))


    def jumped_on(self):
        """When Mario squishes him"""
        if self.state != c.JUMPED_ON:
            self.state = c.JUMPED_ON
            self.frame_index = 2
            self.x_vel = 0
            self.y_vel = 0
            self.rect.y += 16

    def shell_sliding(self):
        pass

