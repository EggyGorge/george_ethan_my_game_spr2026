import pygame as pg
from settings import *
from pygame.sprite import Sprite

class Map:
    def __init__(self, filename):
        #creating the data for building the map using a list
        self.data = []

        # open a file and close with 'with'
        with open(filename, 'rt') as f:
            for line in f: 
                self.data.append(line.strip())

        #
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data[0])
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert() # loads a file and converts it to something usable

    def get_image(self,x,y,width,height):
        image = pg.Surface((width, height)) # screen for image to be drawn on
        image.blit(self.spritesheet, (0,0), (x,y, width, height)) # draws the image on top of the screen
        new_image = pg.transform.scale(image, (width, height)) 
        image = new_image
        return image


# class for cooldown based on tickrate
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.time = time
    def start(self):
        self.start_time = pg.time.get_ticks()
    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than or equal to self.time
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False
    
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


def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill, BAR_HEIGHT)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, BLACK, outline_rect, 2)

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
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.update_image()
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center

    def update(self):
        self.spread()
        self.update_image()


    def update_image(self):
        size = max(1, int(self.radius * 2))
        self.image = pg.Surface((size, size), pg.SRCALPHA) # makes an image for the circle to be drawn on where SRCALPHA makes that image transparent
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        pg.draw.circle(self.image, BLACK, (size // 2, size // 2), int(self.radius), 2)

    def spread(self):
        self.radius += 1
        if self.radius >= self.max_radius:
            self.kill()
    