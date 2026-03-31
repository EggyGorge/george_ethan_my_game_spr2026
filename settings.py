import pygame as pg

# constants for storing values
WIDTH = 800
HEIGHT = 600
TITLE = "My cool game..."
FPS = 60
TILESIZE = 32

# player values
PLAYER_SPEED = 280
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE)

# mob values
MOB_SPEED = 100

# projectile constants
PROJECTILE_SPEED = 400



# tuple storing RGB values for colors
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
TAN = (203, 189, 147)

# health bar
BAR_LENGTH = 100
BAR_HEIGHT = 10