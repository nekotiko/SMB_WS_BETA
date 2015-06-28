from utils.sprite_loader import get_pipe
from utils.constants import BRICK_SIZE_MULTIPLIER, BLACK, WHITE
from utils.sprite_loader import IMAGE_SLIDER

__author__ = 'bakeneko'

import pygame as pg

from utils import constants as c


class BrickPlatform(pg.sprite.Sprite):

    def __init__(self, x, y, image='red_floor'):
        pg.sprite.Sprite.__init__(self)
        self.image = IMAGE_SLIDER.get_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)


class SolidPlatform(BrickPlatform):

    def __init__(self, x, y):
        BrickPlatform.__init__(self, x, y, 'solid_brick')

class Brick(pg.sprite.Sprite):
    """Bricks that can be destroyed"""
    def __init__(self, x, y, setup_frames=None, contents=None, powerup_group=None, name='brick'):
        """Initialize the object"""

        #self.sprite_sheet = setup.GFX['tile_set']
        pg.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        self.opened_frame = None

        if setup_frames:
            setup_frames()
        else:
            self.setup_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)
        self.bumped_up = False
        self.rest_height = y
        self.state = c.RESTING
        self.y_vel = 0
        self.gravity = 1.2
        self.name = name
        self.contents = contents
        self.setup_contents()
        self.group = powerup_group
        self.powerup_in_box = True

    def setup_frames(self):
        """Set the frames to a list"""
        self.frames.append(IMAGE_SLIDER.get_image('red_brick'))
        self.frames.append(IMAGE_SLIDER.get_image('empty_brick'))

    def setup_contents(self):
        """Put 6 coins in contents if needed"""
        if self.contents == '6coins':
            self.coin_total = 6
        else:
            self.coin_total = 0

    def update(self):
        """Updates the brick"""
        self.handle_states()

    def handle_states(self):
        """Determines brick behavior based on state"""
        if self.state == c.RESTING:
            self.resting()
        elif self.state == c.BUMPED:
            self.bumped()
        elif self.state == c.OPENED:
            self.opened()

    def resting(self):
        """State when not moving"""
        if self.contents == '6coins':
            if self.coin_total == 0:
                self.state == c.OPENED

    def bumped(self):
        """Action during a BUMPED state"""
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

        if self.rect.y >= (self.rest_height + 5):
            self.rect.y = self.rest_height
            if self.contents == 'star':
                self.state = c.OPENED
            elif self.contents == '6coins':
                if self.coin_total == 0:
                    self.state = c.OPENED
                else:
                    self.state = c.RESTING
            else:
                self.state = c.RESTING


    def start_bump(self):
        """Transitions brick into BUMPED state"""
        if self.state == c.OPENED:
            return

        self.y_vel = -6

        if self.contents == '6coins':
            #setup.SFX['coin'].play()

            if self.coin_total > 0:
                #self.group.add(coin.Coin(self.rect.centerx, self.rect.y, score_group))
                self.coin_total -= 1
                if self.coin_total == 0:
                    self.frame_index = 0
                    self.frames = self.opened_frame
                    self.image = self.frames[self.frame_index]

        elif self.contents == 'star':
            #setup.SFX['powerup_appears'].play()
            self.frame_index = 0
            self.frames = self.opened_frame
            self.image = self.frames[self.frame_index]

        self.state = c.BUMPED


    def opened(self):
        """Action during OPENED state"""
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        if self.contents == 'star' and self.powerup_in_box:
            #self.group.add(powerups.Star(self.rect.centerx, self.rest_height))
            self.powerup_in_box = False


class QuestionBox(Brick):

    def __init__(self, x, y, level, contents='6coins'):

        Brick.__init__(self, x, y, self.setup_frames, contents)

        self.frame_index = 0
        self.level = level
        self.image = self.frames[self.frame_index]
        self.opened_frame = [IMAGE_SLIDER.get_image('question_mark_3')]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.coin_total = 1
        self.current_time = 0

    def setup_frames(self):
        """Set the frames to a list"""
        for num in xrange(2, -1, -1):
            self.frames.append(IMAGE_SLIDER.get_image('question_mark_{}'.format(num)))
        for num in xrange(0, 3):
            self.frames.append(IMAGE_SLIDER.get_image('question_mark_{}'.format(num)))

    def update(self):

        """Determines brick behavior based on state"""
        if self.state == c.RESTING:
            self.current_time += 5 * self.level.physics_info['seconds']
            if self.current_time > 5:
                self.current_time = 0
            self.frame_index = int(self.current_time)
            self.image = self.frames[self.frame_index]
            self.resting()
        elif self.state == c.BUMPED:
            self.bumped()
        elif self.state == c.OPENED:
            self.opened()



class BrickPiece(pg.sprite.Sprite):
    """Pieces that appear when bricks are broken"""
    def __init__(self, x, y, xvel, yvel):
        super(BrickPiece, self).__init__()
        #self.sprite_sheet = setup.GFX['item_objects']
        self.setup_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_vel = xvel
        self.y_vel = yvel
        self.gravity = .8


    def setup_frames(self):
        """create the frame list"""
        self.frames = []

        image = IMAGE_SLIDER.get_image('broken_brick', multiplier=BRICK_SIZE_MULTIPLIER)
        reversed_image = pg.transform.flip(image, True, False)

        self.frames.append(image)
        self.frames.append(reversed_image)

    def update(self):
        """Update brick piece"""
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.y_vel += self.gravity
        self.check_if_off_screen()

    def check_if_off_screen(self):
        """Remove from sprite groups if off screen"""
        if self.rect.y > c.SCREEN_HEIGHT:
            self.kill()



class Pipe(pg.sprite.Sprite):

    def __init__(self, x, y, size=1):
        pg.sprite.Sprite.__init__(self)
        self.image = get_pipe(size)
        self.rect = self.image.get_rect(bottomleft=(x,y+32))
        self.mask = pg.mask.from_surface(self.image)










