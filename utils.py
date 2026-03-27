import pygame as pg
from settings import *

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
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill, BAR_HEIGHT)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, BLACK, outline_rect, 2)