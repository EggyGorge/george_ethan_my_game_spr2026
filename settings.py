import pygame as pg

# constants for storing values
WIDTH = 1740 #800
HEIGHT = 900 #600
TITLE = "My cool game..."
FPS = 60
TILESIZE = 32

# player values
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE)
BASE_XP_REQUIRED = 100
XP_LEVEL_INCREASE_SCALE = 1.1

# mob values
MOB_SPEED = 100
MOB_SPAWN_COOLDOWN_INITIAL = 3000  # starting cooldown in ms
MOB_SPAWN_FREQUENCY_INCREASE = 500  # ms to reduce per interval
DIFFICULTY_INTERVAL = 30  # seconds between difficulty increases

# powerup values
POWERUP_INTERVAL = 15000
DAMAGE_BOOST_DURATION = 10  # seconds
SPEED_BOOST_DURATION = 10  # seconds

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
LIGHT_BLUE = (173, 216, 230)
DARK_RED = (139, 0, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
DARK_YELLOW = (100, 100, 0)
BROWN = (150,75,0)
GRAY = (205, 198, 180)
GRAY_TWO = (219, 208, 178)
GREEN_GRAY = (180, 184, 179)

# health bar
BAR_LENGTH = 100
BAR_HEIGHT = 10