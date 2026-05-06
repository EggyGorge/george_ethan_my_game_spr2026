import pygame as pg
from pygame.sprite import Sprite
from settings import * 
from sprites import *
from utils import *
from os import path
import math
import random
vec = pg.math.Vector2



class Xp_Boost(Sprite): 
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
            self.game.player.experience_points += 35 * (XP_LEVEL_INCREASE_SCALE * (self.game.player.level - 1))
            self.kill()

class Health_Boost(Sprite): 
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
            if self.game.player.health < self.game.player.max_health:
                self.game.player.health += min(10, self.game.player.max_health - self.game.player.health)
            self.kill()

class Damage_Boost(Sprite): 
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
            self.game.player.activate_damage_boost(2.0, DAMAGE_BOOST_DURATION)
            self.kill()
class Speed_Boost(Sprite): 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect = self.rect.copy()

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.the_player, False, collide_hit_rect)
        if hits:
            self.game.player.speed *= 2
            self.kill()

POWERUPS = [Health_Boost, Xp_Boost, Damage_Boost, Speed_Boost]

def choose_random_powerup(game, x, y):
    chosen_powerup = random.choice(POWERUPS)
    chosen_powerup(game, x, y)