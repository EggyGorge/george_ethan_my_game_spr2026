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

class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.time = time
    def start(self):
        self.start_time = pg.time.get_ticks()
    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False