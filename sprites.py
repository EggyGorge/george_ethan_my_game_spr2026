import pygame as pg
from pygame.sprite import Sprite
from settings import * 
from utils import *
from os import path
from ctypes import Array
from playerstates import *
from statemachine import *
vec = pg.math.Vector2 # importing vectors

# not a method but a function because it applies to all classes
# checks for collision between two entities
def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

# checks for collision with walls and set the position based on the direction of the collision
def collide_with_walls(sprite, group, dir):

    # for the x direction
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
             #print("collided with wall from x dir")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0 # stops movement in x direction
            sprite.hit_rect.centerx = sprite.pos.x 

    # for the y direction
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            #print("collided with wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0 # stops movement in y direction
            sprite.hit_rect.centery = sprite.pos.y

    #if pg.sprite.spritecollide.one.group == projectile:






# class for the player
class Player(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.the_player
        Sprite.__init__(self, self.groups)
        self.game = game
        #self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        #self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE)) # uses constant tilesize for  size
        #self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE) # setting initial image to first in the spritesheet
        #self.image.set_colorkey(BLACK) # black is the color on the sprite that will be transparent
        #self.image = game.player_img
        #self.image.fill(WHITE) # color
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
        self.states: Array[State] = [PlayerIdleState(self), PlayerMoveState(self)]
        self.state_machine.start_machine(self.states)
        # firing cooldown (ms)
        self.fire_cooldown = Cooldown(500)
        self.health = 100

    # movement and actions based on user input
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # for diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071


    #def load_images(self):
        # getting the sprites for idle animation out of spritesheet
        # self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), 
        #                         self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)]
        # # same thing for moving animation
        # self.moving_frames = [self.spritesheet.get_image(TILESIZE*2,0,TILESIZE, TILESIZE), 
        #                       self.spritesheet.get_image(TILESIZE*3,0,TILESIZE, TILESIZE)]
        # self.crawling_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
        #                         self.spritesheet.get_image(TILESIZE*3,0,TILESIZE, TILESIZE)]
        # 
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)
        # for frame in self.moving_frames:
        #     frame.set_colorkey(BLACK)
            
        # for frame in self.crawling_frames:
        #     frame.set_colorkey(BLACK)
        
    # method for animated sprites
    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.moving:
    #         # getting the value to be inputted to the load images for idle 
    #         if now - self.last_update > 350:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.standing_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
    #     # getting the value to be inputted to the load images for moving
    #     elif self.moving:
    #         if now - self.last_update > 350:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.moving_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
        # elif self.crawling:
        #     if now - self.last_update > 350:
        #         self.last_update = now
        #         self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
        #         bottom = self.rect.bottom
        #         self.image = self.moving_frames[self.current_frame]
        #         self.rect = self.image.get_rect()
        #         self.rect.bottom = bottom
        
    
    def state_check(self):
        # if the player's velocity is not zero, then the player is moving and state will be changed in the state machine
        if self.vel != vec(0,0): 
            self.moving = True
            self.state_machine.transition("move")
        # if the player's velocity is  zero, then the player is idle and state will be changed in the state machine
        else: 
            self.moving = False
            self.state_machine.transition("idle")



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

# mobs in a class
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.speed = MOB_SPEED
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.pos
        self.rect.center = self.pos
        self.health = 100
        

    def update(self):
        # chase the player, using dt for smooth movement
        direction = self.game.player.pos - self.pos
        if direction.length_squared() != 0:
            self.vel = direction.normalize()
        else:
            self.vel = vec(0, 0)

        # X axis movement + collision
        self.pos.x += self.vel.x * self.speed * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')

        # Y axis movement + collision
        self.pos.y += self.vel.y * self.speed * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        hits = pg.sprite.spritecollide(self, self.game.the_player, False, collide_hit_rect)
        if hits:
            self.game.player.health -= 25
            self.kill()

        self.rect.center = self.hit_rect.center
        
        if self.health <= 0:
            self.kill()

class Projectile(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) 
        self.rect.center = self.pos
        self.hit_rect = self.rect.copy() # give the projectile a hit_rect for collision checks

        # convert mouse position from screen coordinates to world coordinates
        mouse_pos = vec(pg.mouse.get_pos()) + self.game.camera
        direction = mouse_pos - self.pos
        # avoids division by 0 if player happens to click exactly 
        if direction.length_squared() == 0: 
            direction = vec(1, 0)
        else:
            direction = direction.normalize() # sets vector to be length 1 so velocity can be equal in all scenarios
        self.vel = direction * PROJECTILE_SPEED

        
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
                mob.health -= 50
                if mob.health <= 0:
                     mob.kill()
            self.kill()
        # removes projectile if it goes offscreen
        if (self.rect.right < 0 + self.game.camera.x or self.rect.left > WIDTH + self.game.camera.x or self.rect.bottom < 0 + self.game.camera.y or self.rect.top > HEIGHT + self.game.camera.y):
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
    def update(self):
        pass

# coin class
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
    def update(self):
        pass