import pygame
import random

"""
Static global variables
"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

width_window = 1800
height_window = 1000

fps = 30

win = pygame.display.set_mode((width_window, height_window))  # главный игровой экран


"""
Dynamic global variables
"""
maingunlist = []

blocksdict = {1: (650, 1190, 170, 245), 2: (1030, 1150, 300, 420), 3: (1330, 1390, 410, 480),
              4: (1260, 1400, 480, 777), 5: (1310, 1367, 780, 920), 6: (480, 550, 250, 300),
              7: (450, 480, 280, 350), 8: (400, 450, 350, 490), 9: (390, 440, 600, 730),
              10: (400, 450, 700, 800), 11: (410, 470, 800, 900), 12: (540, 1270, 950, 1000)}


