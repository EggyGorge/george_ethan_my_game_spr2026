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
        
        self.angle = angle  # (in degrees) sets the angle around the player at which the circler is added
        self.radius = radius # how far away from the player the circler is
        self.angular_speed = angular_speed  # degrees of rotation per second
        
        self.pos = vec(0, 0)
        self.hit_rect = None
        
        # track last time each mob was damaged by this circler to prevent spam damage
        self.mob_hit_times = {}  # maps mob to last hit time in dictionary
        self.damage_cooldown = 0.5  # seconds between hits on the same mob

        self.duration = 10  # seconds the circler is active
        self.elapsed_time = 0
        self.is_active = True  # track if circler is currently active
        self.cooldown = Cooldown(10000)  # time between circler activations

        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Circler_ability.png"))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        
        self.update_image()
        
    def update_image(self):       
        if self.is_active:
            self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
            self.image.set_colorkey(BLACK)
        else: # create dimmed version for inactive state
            self.image.copy
            self.image.set_colorkey(BLACK)
            # Create a dimmed surface by blitting a semi-transparent dark overlay
            dark_overlay = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA) # SRCALPHA allows for the a in RGBA (the transparency factor)
            dark_overlay.fill((0, 0, 0, 128)) # 50% opacity overlay creates dimming effect
            self.image.blit(dark_overlay, (0, 0)) # puts the dark overlay over the image
        
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()
        
    def kill(self):
        self.player.remove_circler(self)
        Sprite.kill(self)

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
        
        if self.is_active:
            # track how long the circler has been active
            self.elapsed_time += self.game.dt
            
            # when duration expires, deactivate and start cooldown
            if self.elapsed_time >= self.duration:
                self.is_active = False
                self.elapsed_time = 0
                if self == self.player.circlers[0]:  # only the first circler manages the cooldown
                    self.cooldown.start()
                self.update_image()
                return
            
            # check collision with mobs - damage them only when active
            mob_hits = pg.sprite.spritecollide(self, self.game.all_mobs, False, collide_hit_rect)
            current_time = pg.time.get_ticks() / 1000  # convert to seconds
            for mob in mob_hits:
                # Only damage each mob if enough time has passed since last hit
                last_hit = self.mob_hit_times.get(mob, -self.damage_cooldown)
                if current_time - last_hit >= self.damage_cooldown:
                    damage = int(50 * self.player.get_damage_multiplier())
                    if hasattr(mob, 'take_damage'):
                        mob.take_damage(damage)
                    else:
                        mob.health -= damage
                    self.mob_hit_times[mob] = current_time
                    if mob.health <= 0:
                    #     mob.kill()
                        self.mob_hit_times.pop(mob, None)  # clean up dead mobs from dictionary
        else:
            # in cooldown state - check if cooldown is ready to reactivate
            if self.player.circlers[0].cooldown.ready():  # all use the first circler's cooldown
                self.is_active = True
                self.elapsed_time = 0
                self.update_image()


class CirclerAttack: # add one circler around the player each time the ability is chosen
    def __init__(self, game, player, radius=80, angular_speed=360):
        self.game = game
        self.player = player
        self.player.add_circler(radius, angular_speed)

    def kill_all(self): # placeholder if future logic needs to remove all circlers
        for circler in list(self.player.circlers):
            circler.kill()

class Forcefield(Sprite):
    def __init__(self, game, player, radius=150):
        self.groups = game.all_sprites, game.all_forcefields
        Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.radius = radius
        self.cooldown = Cooldown(15000)  # time between forcefield activations
        self.slow_factor = 0.5  # mobs move at 50% speed in the forcefield
        self.duration = 10  # seconds the forcefield lasts when active
        self.elapsed_time = 0
        self.is_active = True  # track if forcefield is currently active
        self.update_image()
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center

    def update_image(self):
        size = self.radius * 2
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        # Draw the circle differently based on active/inactive state
        if self.is_active: # dimmed when inactive
            color = PURPLE
        else:
            color = WHITE
        pg.draw.circle(self.image, color, (size // 2, size // 2), int(self.radius), 2)
        self.rect = self.image.get_rect()
        self.rect.center = self.player.pos
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center

    def update(self): # helped by AI Claude Haiku 4.5 agent built into VScode: "Could you help me make the forcefield reappear after the cooldown?"
        # keeps the forcefield centered on the player
        self.rect.center = self.player.pos
        self.hit_rect.center = self.player.pos
        
        if self.is_active:
            # tracks how long the forcefield has been active
            self.elapsed_time += self.game.dt
            
            # when duration expires, deactivate and start cooldown
            if self.elapsed_time >= self.duration:
                self.is_active = False
                self.elapsed_time = 0
                self.cooldown.start()
                self.update_image()
        else:
            # in cooldown state - check if cooldown is ready to reactivate
            if self.cooldown.ready():
                self.is_active = True
                self.elapsed_time = 0
                self.update_image()
        



     
        

class Xp_Gain_Boost: # increases the amount of xp the player gets per experience orb
    def __init__(self, game, player):
        self.game = game
        self.game.player.xp_gain += 25
            
class Health_Gain_Boost: # increases the speed the player regens health over time
    def __init__(self, game, player):
        self.game = game
        self.game.player.regen_factor += 3/5

class Max_Health_Boost: # increases the player's max health 
    def __init__(self, game, player):
        self.game = game
        self.game.player.max_health += 10