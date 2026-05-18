import pygame as pg
from pygame.sprite import Sprite
from settings import * 
from utils import *
from os import path
from ctypes import Array
from playerstates import *
from statemachine import *
from abilities import *
vec = pg.math.Vector2 # importing vectors

# # not a method but a function because it applies to all classes
# # checks for collision between two entities
# def collide_hit_rect(one,two):
#     return one.hit_rect.colliderect(two.rect)

# # checks for collision with walls and set the position based on the direction of the collision
# def collide_with_walls(sprite, group, dir):

#     # for the x direction
#     if dir == "x":
#         hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
#         if hits:
#              #print("collided with wall from x dir")
#             if hits[0].rect.centerx > sprite.hit_rect.centerx:
#                 sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
#             if hits[0].rect.centerx < sprite.hit_rect.centerx:
#                 sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
#             sprite.vel.x = 0 # stops movement in x direction
#             sprite.hit_rect.centerx = sprite.pos.x 

#     # for the y direction
#     if dir == "y":
#         hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
#         if hits:
#             #print("collided with wall from y dir")
#             if hits[0].rect.centery > sprite.hit_rect.centery:
#                 sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
#             if hits[0].rect.centery < sprite.hit_rect.centery:
#                 sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
#             sprite.vel.y = 0 # stops movement in y direction
#             sprite.hit_rect.centery = sprite.pos.y







# class for the player
class Player(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.the_player
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)) # uses constant tilesize for  size
        self.rect = self.image.get_rect() # shape
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT

        # creating variables for states when the game loads and setting them to false
        self.walking = False
        self.moving = False
        # self.crawling = False
        self.jumping = False

        # creatign variables for the frames that will be used to decide the player's appearance at a given time
        self.last_update = 0
        self.current_frame = 0

        # including the state machine stuff
        self.state_machine = StateMachine()
        # track which direction the player is facing for sprite selection
        # possible values: 'left', 'right'
        self.facing = 'right'
        self.states: Array[State] = [PlayerIdleState(self), PlayerMoveState(self)]
        self.state_machine.start_machine(self.states)
        self.fire_cooldown = Cooldown(500) # firing cooldown (ms)
        self.shockwave_cooldown = Cooldown(5000)
        self.speed = PLAYER_SPEED
        self.max_health = 100
        self.health = 100
        self.regen_factor = 3/5
        self.experience_points = 0
        self.level = 1
        self.xp_needed = BASE_XP_REQUIRED
        self.level_up_flag = False
        self.mobs_defeated = 0
        self.xp_gain = 50
        self.damage_boost_multiplier = 1.0
        self.damage_boost_end_time = 0
        self.speed_boost_multiplier = 1.0
        self.speed_boost_end_time = 0
        self.circlers = []
        self.shockwave_count = 0

    def add_circler(self, radius=80, angular_speed=180):
        if len(self.circlers) >= 6: # caps amount of circlers the player can have
            return
        circler = Circler(self.game, self, 0, radius, angular_speed) # adds a circler around the player
        self.circlers.append(circler) # adds circler to player's list of circlers to keep track 
        self.sync_circlers()  # sync all circlers' state
        self.rebalance_circlers()

    def sync_circlers(self):
        # sync all circlers to the same elapsed_time and is_active state
        if len(self.circlers) == 0:
            return
        first_circler = self.circlers[0]
        for circler in self.circlers:
            circler.elapsed_time = first_circler.elapsed_time
            circler.is_active = first_circler.is_active
            circler.update_image()

    def remove_circler(self, circler):
        if circler in self.circlers:
            self.circlers.remove(circler)
            self.rebalance_circlers()

    def rebalance_circlers(self): # makes sure all the circlers around the player are evenly spaced
        count = len(self.circlers)
        if count == 0:
            return
        angle_offset = 360 / count
        for i, circler in enumerate(self.circlers): # gives each circler the necessary amount of angle offset to be equally spaced
            circler.angle = i * angle_offset 


    # movement and actions based on user input
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        speed = self.speed * self.get_speed_multiplier()
        if keys[pg.K_a]:
            self.vel.x = -speed
            self.facing = 'left'
        if keys[pg.K_d]:
            self.vel.x = speed
            self.facing = 'right'
        if keys[pg.K_w]:
            self.vel.y = -speed
        if keys[pg.K_s]:
            self.vel.y = speed
        if keys[pg.K_q]:
            if self.shockwave_cooldown.ready() and self.shockwave_count>0:
                Shockwave(self.game, self.pos.x, self.pos.y, TILESIZE/2, 50, self)
                self.shockwave_count -= 1
                self.shockwave_cooldown.start()
        # for diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    
    def state_check(self):
        # if the player's velocity is not zero, then the player is moving and state will be changed in the state machine
        if self.vel != vec(0,0): 
            self.moving = True
            self.state_machine.transition("move")
        # if the player's velocity is  zero, then the player is idle and state will be changed in the state machine
        else: 
            self.moving = False
            self.state_machine.transition("idle")

    def check_level_up(self):
        if self.experience_points >= self.xp_needed:
            self.level += 1
            old_xp_needed = self.xp_needed # used for avoiding negative xp when calculating overflow xp
            self.xp_needed = BASE_XP_REQUIRED * ((self.level - 1) * XP_LEVEL_INCREASE_SCALE)
            self.experience_points = self.experience_points - old_xp_needed # to carry over xp from last level to the current on level up
            self.level_up_flag = True
            
    def activate_damage_boost(self, multiplier, duration):
        self.damage_boost_multiplier = multiplier
        self.damage_boost_end_time = pg.time.get_ticks() + int(duration * 1000) # gets the current time of the game and finds what time the ability should end based on the duration

    def update_damage_boost(self):
        if self.damage_boost_multiplier != 1.0 and pg.time.get_ticks() >= self.damage_boost_end_time:
            self.damage_boost_multiplier = 1.0

    def get_damage_multiplier(self):
        return self.damage_boost_multiplier

    def activate_speed_boost(self, multiplier, duration):
        self.speed_boost_multiplier = multiplier
        self.speed_boost_end_time = pg.time.get_ticks() + int(duration * 1000)

    def update_speed_boost(self):
        if self.speed_boost_multiplier != 1.0 and pg.time.get_ticks() >= self.speed_boost_end_time:
            self.speed_boost_multiplier = 1.0

    def get_speed_multiplier(self):
        return self.speed_boost_multiplier


    # when the game updates it takes user key inputs, changes objectws pos, and player position based on velovity and tickrate
    def update(self):
        self.state_machine.update()
        self.get_keys()
        self.state_check()
        #self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        # uses the seperate x and y direction functions to change the colliding objects post-collision position
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center 

        if pg.sprite.spritecollide(self, self.game.all_experience, True, collide_hit_rect):
            self.experience_points += self.xp_gain
        self.check_level_up()
        self.update_damage_boost()
        self.update_speed_boost()

        # regenerates player's health but caps at max health
        if self.health < self.max_health:
            self.health += self.regen_factor * self.game.dt
        

# mobs in a class
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Mob Sprite.png"))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.speed = MOB_SPEED
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.pos
        self.rect.center = self.pos
        self.health = 100
        self.damage = 10
        self.is_flashing = False
        self.flash_duration = 150  # milliseconds
        self.flash_end_time = 0

    def take_damage(self, amount):
        self.health -= amount
        self.is_flashing = True
        self.flash_end_time = pg.time.get_ticks() + self.flash_duration

    def update(self):
        # chase the player, using dt for smooth movement
        if self.is_flashing: # has the mob have a red overlay if it is damaged and the end time for the flashing hasn't ended yet
            if pg.time.get_ticks() < self.flash_end_time:
                self.image = self.base_image.copy()
                flash = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
                flash.fill((255, 0, 0, 120))
                self.image.blit(flash, (0, 0), special_flags=pg.BLEND_RGBA_ADD)
                self.image.set_colorkey(BLACK)
            else: # reverts to base if the flashing is over
                self.is_flashing = False
                self.image = self.base_image.copy()
                self.image.set_colorkey(BLACK)

        direction = self.game.player.pos - self.pos
        if direction.length_squared() != 0:
            self.vel = direction.normalize()
        else:
            self.vel = vec(0, 0)

        # check if mob is in a forcefield and apply slowdown
        current_speed = self.speed
        forcefield_hits = pg.sprite.spritecollide(self, self.game.all_forcefields, False, collide_hit_rect)
        if forcefield_hits and forcefield_hits[0].is_active: # apply the slowdown factor from the forcefield only if it's active
            current_speed *= forcefield_hits[0].slow_factor

        # X axis movement + collision
        self.pos.x += self.vel.x * current_speed * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')

        # Y axis movement + collision
        self.pos.y += self.vel.y * current_speed * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        hits = pg.sprite.spritecollide(self, self.game.the_player, False, collide_hit_rect)
        if hits:
            self.game.player.health -= self.damage
            self.kill()

        self.rect.center = self.hit_rect.center
        
        if self.health <= 0:
            Experience(self.game, self.pos.x, self.pos.y)
            self.game.player.mobs_defeated += 1
            self.kill()
        
        
            

class Projectile(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        # determine shot direction (world coords)
        self.pos = vec(x,y)
        # convert mouse coordinates to world coordinates
        mouse_pos = vec(pg.mouse.get_pos()) + self.game.camera 
        direction = mouse_pos - self.pos
        if direction.length_squared() == 0: # avoids division by zero if a player happens to click exactly
            direction = vec(1, 0)
        else:
            direction = direction.normalize() # sets vector to be length 1 so velocity can be equal across all directions
        self.vel = direction * PROJECTILE_SPEED

        self.projectile_damage = 50

        # select a sprite frame from the Nerd Sprite sheet based on direction
        proj_x_map = {
            'right': 0,
            'left': TILESIZE,
            'down': TILESIZE * 2,
            'up': TILESIZE * 3,
        }
        if abs(direction.x) > abs(direction.y):
            dstr = 'right' if direction.x > 0 else 'left'
        else:
            dstr = 'down' if direction.y > 0 else 'up'

        try:
            self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Nerd Sprite.png"))
            col_x = proj_x_map.get(dstr, 0)
            self.image = self.spritesheet.get_image(col_x, TILESIZE, TILESIZE, TILESIZE)
            self.image.set_colorkey(BLACK)
        except Exception:
            # fallback to a simple red square if loading fails
            self.image = pg.Surface((TILESIZE, TILESIZE))
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect.copy()

        
    def update(self):
        self.pos += self.vel * self.game.dt # use delta time so speed is fps-independent
        # match visual and collision
        self.rect.center = self.pos
        self.hit_rect.center = self.pos

        # remove projectile if it hits a wall
        if pg.sprite.spritecollide(self, self.game.all_walls, False, collide_hit_rect):
            self.kill()
        # remove projectile and damage mob if they collide
        mob_hits = pg.sprite.spritecollide(self, self.game.all_mobs, False, collide_hit_rect)
        if mob_hits:
            for mob in mob_hits:
                mob.take_damage(int(self.projectile_damage * self.game.player.get_damage_multiplier()))
            self.kill()
        # removes projectile if it goes offscreen
        if (self.rect.right < 0 + self.game.camera.x or self.rect.left > WIDTH + self.game.camera.x or self.rect.bottom < 0 + self.game.camera.y or self.rect.top > HEIGHT + self.game.camera.y):
            self.kill()

class Shockwave(Sprite):
    def __init__(self, game, x, y, radius, damage, owner):
        self.groups = game.all_sprites, game.all_shockwaves
        Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.damage = damage
        self.radius = radius
        self.max_radius = radius * 20
        self.owner = owner
        self.mobs_hit = set()
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.update_image()
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center

    def update(self):
        self.spread()
        self.update_image()
        self.apply_damage()

    def apply_damage(self):
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False, collide_hit_rect)
        for mob in hits:
            if mob not in self.mobs_hit:
                mob.take_damage(int(self.damage * self.owner.get_damage_multiplier()))
                self.mobs_hit.add(mob)
                # if mob.health <= 0:
                #     mob.kill()
                    

    def update_image(self):
        size = max(1, int(self.radius * 2))
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        pg.draw.circle(self.image, BLACK, (size // 2, size // 2), int(self.radius), 2)

    def spread(self):
        self.radius += 1
        if self.radius >= self.max_radius:
            self.kill()

# walls in a class
class Wall(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        # pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = (0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos

# experience class
class Experience(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_experience
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Experience.png"))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.last_update = pg.time.get_ticks()
        self.frame = 0
        self.animation_speed = 250

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            self.frame = (self.frame + 1) % 2
            if self.frame == 0:
                self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.spritesheet.get_image(0, TILESIZE, TILESIZE, TILESIZE)
            self.image.set_colorkey(BLACK)