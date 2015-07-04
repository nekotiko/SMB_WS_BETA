__author__ = 'bakeneko'

import pygame



# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode([screen_width, screen_height])

logo = pygame.image.load('sega_logo.png')
sound = pygame.mixer.Sound('sega_sound.ogg')
sound_channel = None

logo_y = (screen_height / 2) - (logo.get_rect().height / 2)
logo_slice = [0, 0, 15, logo.get_rect().height]

PIXELS_PER_SECOND = 300
LOGO_WIDTH = 600
FPS = 60
end_logo = False
clock = pygame.time.Clock()
total_seconds = 0

change_x = 0

while not end_logo:
    time_in_millis = clock.tick(FPS)
    seconds = time_in_millis / 1000.0
    total_seconds += seconds

    screen.fill(pygame.Color('white'))
    if logo_slice[0] <= LOGO_WIDTH:

        logo_part = pygame.Surface(logo_slice[2:4],  pygame.SRCALPHA, 32)

        logo_part.blit(logo, (0, 0), logo_slice)
        screen.blit(logo_part, (int(logo_slice[0]), logo_y))
        logo_slice[0] += PIXELS_PER_SECOND * seconds

    else:
        if not sound_channel:
            sound_channel = sound.play()

        screen.blit(logo, (20, logo_y))

    pygame.display.flip()

    if total_seconds > 4:
        end_logo = True


pygame.quit()
