'''
Main file responsible for game loop including input, update, and draw methods.
'''
# I can push from VS Code

import pygame as pg
import sys
from os import path # accesses file system of the operating system
from settings import *
from utils import *
from sprites import *
vec = pg.math.Vector2

# the game class that will be instantiated in order to run the game
class Game:
    def __init__(self):
        pg.init()
        # setting up pygame screen using tuple value for width and height
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(5000)


# a method is a function tied to a Class
    def load_data(self):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.wall_img = pg.image.load(path.join(self.img_dir, 'wall.png')).convert_alpha()
        # self.player_img = pg.image.load(path.join(self.img_dir, 'blocky_left-scaled.png')).convert_alpha()
        self.map = Map(path.join(self.game_dir, 'level1.txt'))
        print('data is loaded')

    def new(self):
        self.load_data()

        # making all sprite, walls, mobs, etc. sprite groups
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()

        # self.player = Player(self, 15, 15)
        # self.mob = Mob(self, 5,5)
        # self.goal = Goal(self, WIDTH/2 * TILESIZE, HEIGHT/2 * TILESIZE)

        # loop to draw tiles on screen based on txt file
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    # call class constructor without assigning a variable
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    self.mob = Mob(self,col,row)
        self.run()

        
    # makes sure other methods occur while the program is running
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 # the passing of time in the proper tickrate
            self.events()
            self.update()
            self.draw()

    def events(self):
        # stuff that happens with "peripherals" - keyboard, mouse
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False # ends the game when it needs to be quit
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
               print("I can get mouse input.")
               print(event.pos) # prints mouse's current coordinate
            if event.type == pg.KEYUP:
                if event.key == pg.K_k:
                    print("I can print when the K key is pressed.")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_k:
                    print("I can print when the K key is down.")

                # if event.key == pg.K_w: # move up when W key is pressed
                #     self.player.rect.y -= 2
                # if event.key == pg.K_a: # move left when S key is pressed
                #     self.player.rect.x -= 2
                # if event.key == pg.K_d: # move right when D key is pressed
                #     self.player.rect.x += 2 
                # if event.key == pg.K_s:
                #     self.player.rect.y += 2
                # if event.key == pg.K_t:
                #     self.player.image.fill(RED)
                # if event.key == pg.K_SPACE and pg.K_s:
                #     self.player.rect.y += 20



    def update(self):
        # self.player.rect.x += 1
        # if self.game_cooldown.ready():
        #     print("Cooldown done!")
        #     self.game_cooldown.start
        self.all_sprites.update()
        self.all_walls.update()
        


    def quit(self):
        pass

    # method that drawswhat needs to be drawn like text and sprites
    def draw(self):
        self.screen.fill(BLUE)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
       # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.all_sprites.draw(self.screen)
        pg.display.flip() # so that a new frame can be drawn behind the current one

    # method for drawing text based on things like font, size color, position
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()

pg.quit()

