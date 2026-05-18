from statemachine import *
from settings import *
import pygame as pg
from utils import Spritesheet
from os import path

# idle player state
class PlayerIdleState(State):
    def __init__(self, player):
        self.player = player
        self.name = "idle"
        self.spritesheet = Spritesheet(path.join(self.player.game.img_dir, "Nerd Sprite.png"))
        

    # name of state is idle
    def get_state_name(self):
        return "idle"
    # begins idle state with a white fill for the square
    def enter(self):
        # choose row based on last facing direction and column 0 for standing frame
        direction_rows = {
            'left': 0,
            'right': TILESIZE,
        }
        col_x = direction_rows.get(self.player.facing)
        self.player.image = self.spritesheet.get_image(col_x, 0, TILESIZE, TILESIZE)
        self.player.image.set_colorkey(BLACK)
        print('enter player idle state')

    def exit(self):
        print('exit player idle state')

# keeps filling with white while idle
    def update(self):
        # print('updating player idle state...')
        direction_rows = {
            'left': 0,
            'right': TILESIZE,
        }
        col_x = direction_rows.get(self.player.facing)
        self.player.image = self.spritesheet.get_image(col_x, 0, TILESIZE, TILESIZE)
        self.player.image.set_colorkey(BLACK)
        # self.spritesheet.get_image(0,0, TILESIZE, TILESIZE)
        keys = pg.key.get_pressed()
        # if keys[pg.K_k]:
        #     print('transitioning to attack state...')
        #     self.player.state_machine.transition("attack")
            
class PlayerMoveState(State):
    def __init__(self, player):
        self.player = player
        self.name = "move"
        self.spritesheet = Spritesheet(path.join(self.player.game.img_dir, "Nerd Sprite.png"))


    # name of state is moving
    def get_state_name(self):
        return "move"
    # player's color  before it moves is white
    def enter(self): # sprite facing was helped by AI built into VScode
        direction_rows = {
            'left': TILESIZE * 2,
            'right': TILESIZE * 3,
        }
        col_x = direction_rows.get(self.player.facing)
        self.player.image = self.spritesheet.get_image(0, col_x, TILESIZE, TILESIZE)
        self.player.image.set_colorkey(BLACK)
        print('enter player move state')

    def exit(self):
        print('exit player move state')
    # player's color will be green as it stays in movement
    def update(self):
        # print('updating player move state...')
        direction_rows = {
            'left': TILESIZE * 2,
            'right': TILESIZE * 3,
        }
        col_x = direction_rows.get(self.player.facing)
        # column TILESIZE is the running frame
        self.player.image = self.spritesheet.get_image(col_x, 0, TILESIZE, TILESIZE)
        self.player.image.set_colorkey(BLACK)
        keys = pg.key.get_pressed()
  