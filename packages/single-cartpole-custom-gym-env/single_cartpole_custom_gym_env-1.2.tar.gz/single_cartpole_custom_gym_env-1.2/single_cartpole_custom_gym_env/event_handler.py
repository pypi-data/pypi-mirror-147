import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

def pygame_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
