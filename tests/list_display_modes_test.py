import pygame


pygame.init()

# get the modes
a_modes = pygame.display.list_modes()

for mode in a_modes:
    print(f"Mode: {mode}")
pygame.quit()
