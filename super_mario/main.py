from utils.level_loader import load_level

__author__ = 'bakeneko'

import pygame

import utils.constants as config
import levels

from mario import Mario

def main():
    """ Main Program """
    pygame.init()
    FPS = 120

    # Set the height and width of the screen

    screen = pygame.display.set_mode(config.SIZE)

    pygame.display.set_caption("Super Mario Bros!")

    # Create the player
    player = Mario()


    # Set the current level
    current_level_no = 1
    current_level = levels.Level(player)

    load_level(current_level)

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 120
    #Player always starts in the same point
    player.rect.y = config.SCREEN_HEIGHT - player.rect.height - 64
    active_sprite_list.add(player)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:

        #Set Level Physics
        milliseconds =  clock.tick(FPS)
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime = current_level.physics_info['play_time'] + seconds
        current_level.physics_info = {'current_time': milliseconds,
                                      'seconds': seconds,
                                       'play_time': playtime
                                      }


        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player.is_running = True
                if event.key == pygame.K_a and player.state != config.MARIO_STATE_JUMPING:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player.is_running = False
                if event.key == pygame.K_a:
                    player.fight_gravity = False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.go_left()
        if keys[pygame.K_RIGHT]:
            player.go_right()
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

       # If the player gets near the right side, shift the world left (-x)
        LIMIT = config.SCREEN_WIDTH - config.SCREEN_PLAYER_OFFSET
        if player.rect.x >= LIMIT:
            diff = player.rect.x - LIMIT
            player.rect.x = LIMIT
            current_level.shift_world(-diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift


        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)


        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT




        #print(current_level.physics_info)
        """
        pygame.display.set_caption("Millis({})/Seconds({})/PlayTime({}) limit FPS to {} (now: {:.2f})".format(
                       milliseconds, seconds, playtime, FPS,clock.get_fps()))
        """
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()