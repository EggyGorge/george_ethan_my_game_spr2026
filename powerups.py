import pygame as pg
from pygame.sprite import Sprite
from settings import * 
from sprites import *
from utils import *
from os import path
import math
import random
vec = pg.math.Vector2



class Xp_Gain_Boost(Sprite): 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_BLUE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect = self.rect.copy()

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.the_player, False, collide_hit_rect)
        if hits:
            self.game.player.xp_gain += 25
            self.kill()

class Health_Gain_Boost(Sprite): 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect = self.rect.copy()

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.the_player, False, collide_hit_rect)
        if hits:
            self.game.player.regen_factor += 9/5
            self.kill()

class Max_Health_Boost(Sprite): 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect = self.rect.copy()

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.the_player, False, collide_hit_rect)
        if hits:
            self.game.player.max_health += 10
            self.kill()

# POWERUPS = [Xp_Gain_Boost, Health_Gain_Boost, Max_Health_Boost]
POWERUPS = [Max_Health_Boost]

def choose_random_powerup(game, x, y):
    chosen_powerup = random.choice(POWERUPS)
    chosen_powerup(game, x, y)