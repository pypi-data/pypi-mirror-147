import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

def pygame_events(space, myenv, change_target):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if change_target == True and event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            myenv.change_target_point(x, 800-y)
