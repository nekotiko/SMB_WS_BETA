
__author__ = 'bakeneko'

import pygame
import os
from utils.constants import MUTE


data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..','..', 'assets'))

def filepath(filename):
    return os.path.join(data_dir, filename)


def get_font(size):
    font = pygame.font.Font(filepath('font/font.ttf'), size)
    return font


def play_sound(filename, volume=0.5):
    filename = filepath('sound/' + filename)
    if MUTE:
        volume = 0
    try:
        sound = pygame.mixer.Sound(filename)
        sound.set_volume(volume)
        sound.play()
    except:
        raise SystemExit, "Unable to load: " + filename
    return sound


def play_music(filename, volume=0.5, loop=-1):
    filename = filepath('music/' + filename)
    if MUTE:
        volume = 0
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
    except:
        raise SystemExit, "Unable to load: " + filename

def stop_music():
    pygame.mixer.music.stop()

def mute():
    if pygame.mixer.get_volume:
        pygame.mixer.set_volume(0)
    else:
        pygame.mixer.set_volume(0.5)
