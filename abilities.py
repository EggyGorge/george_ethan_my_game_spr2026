import pygame as pg
from pygame.sprite import Sprite
from settings import * 
from utils import *
from os import path
import math
vec = pg.math.Vector2


class Circler(Sprite):
    def __init__(self, game, player, angle, radius=80, angular_speed = 90):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.image = pg.Surface((TILESIZE // 2, TILESIZE // 2))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        
        self.angle = angle  # (in degrees) sets the angle around the player at which the circler is added
        self.radius = radius # how far away from the player the circler is
        self.angular_speed = angular_speed  # degrees of rotation per second
        
        self.pos = vec(0, 0)
        self.hit_rect = self.rect.copy()
        
        # track which mobs have already been hit this frame to avoid repeated damage
        self.hit_mobs = set()
        
    def update(self):
        # rotate the angle based on delta time
        self.angle += self.angular_speed * self.game.dt
        self.angle = self.angle % 360  # keep angle in 0-360 range
        
        # convert angle to radians in order to find orbital position using unit circle
        angle_rad = math.radians(self.angle)
        offset_x = self.radius * math.cos(angle_rad)
        offset_y = self.radius * math.sin(angle_rad)
        
        # position relative to player
        self.pos = self.player.pos + vec(offset_x, offset_y)
        
        # update rects
        self.rect.center = self.pos
        self.hit_rect.center = self.pos
        
        # # check collision with walls - remove if hit
        # if pg.sprite.spritecollide(self, self.game.all_walls, False, collide_hit_rect):
        #     self.kill()
        #     return
        
        # check collision with mobs - damage them (needs more work)
        mob_hits = pg.sprite.spritecollide(self, self.game.all_mobs, False, collide_hit_rect)
        for mob in mob_hits:
            # Only damage each mob once per frame
            if mob not in self.hit_mobs:
                mob.health -= 25
                self.hit_mobs.add(mob)
                if mob.health <= 0:
                    mob.kill()
        
        # clear the hit tracking each frame to allow continuous damage
        self.hit_mobs.clear()


class CirclerAttack: # three circlers around the player
    
    def __init__(self, game, player, num_circlers=3, radius=80, angular_speed=180):
        self.game = game
        self.player = player
        self.circlers = [] # list to hold the individual circlers so they can be referred to as a group
        
        # Evenly space the circlers around the player
        angle_offset = 360 / num_circlers
        for i in range(num_circlers):
            initial_angle = i * angle_offset # changes offset based on which of the circlers it is
            circler = Circler(game, player, initial_angle, radius, angular_speed) 
            self.circlers.append(circler) # adds a circler to the circler group
    
    def kill_all(self): # placeholder for now
        for circler in self.circlers:
            circler.kill()
        self.circlers.clear()

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