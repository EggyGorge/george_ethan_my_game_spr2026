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
import random
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
        self.paused = False
        self.mob_spawn_cooldown = Cooldown(3000)
        self.camera = vec(0, 0) # camera position (top-left corner of the camera view)


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
        self.all_projectiles = pg.sprite.Group()
        self.the_player = pg.sprite.Group()

        # self.player = Player(self, 15, 15)
        
        Mob(self, random.randint(0, WIDTH//TILESIZE), random.randint(0, HEIGHT//TILESIZE)) # spawns a mob randomly on the screen
        self.mob_spawn_cooldown.start() 

        # self.goal = Goal(self, WIDTH/2 * TILESIZE, HEIGHT/2 * TILESIZE)

        # loop to draw tiles on screen based on txt file
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    # call class constructor without assigning a variable
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                # if tile == 'M':
                #     Mob(self,col,row)
                #     self.mob_spawn_cooldown.start()
        self.run()

        
    # makes sure other methods occur while the program is running
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 # the passing of time in the proper tickrate
            self.events()
            if not self.paused:
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
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: # ensuring that the mouse is left clicked
                    if self.player.fire_cooldown.ready():  # fire only if player's cooldown is ready
                        Projectile(self, self.player.pos.x, self.player.pos.y)
                        self.player.fire_cooldown.start()
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                        


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
        self.all_mobs.update()
        self.all_projectiles.update()
        
        
        # spawns mobs in the game update to avoid killing the old mob because of overlap
        if self.mob_spawn_cooldown.ready():  # spawn only if spawn cooldown has been reached
            Mob(self,random.randint(0, WIDTH//TILESIZE), random.randint(0, HEIGHT//TILESIZE))
            self.mob_spawn_cooldown.start()
        
        # update camera to follow player
        self.update_camera()

        if self.player.health <= 0:
            self.running = False
    
    def update_camera(self):
        # center the camera on the player
        self.camera.x = self.player.pos.x - WIDTH / 2
        self.camera.y = self.player.pos.y - HEIGHT / 2
        
        
        


    def quit(self):
        pass

    # method that draws what needs to be drawn like text and sprites
    def draw(self):
        self.screen.fill(TAN)
        # draw sprites with camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera.x, sprite.rect.y - self.camera.y))
        
        # draw health bar with camera offset
        draw_health_bar(self.screen, self.player.pos.x - self.camera.x - BAR_LENGTH/2, self.player.pos.y - self.camera.y + BAR_HEIGHT*2, self.player.health)
        
        # UI text (these should stay in fixed screen positions, so no camera offset)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
       # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        pg.display.flip() # so that a new frame can be drawn behind the current one

    # method for drawing text based on things like font, size color, position
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("The Journey", 48, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to start...", 24, WHITE, WIDTH/2, HEIGHT/2 + HEIGHT/4)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

if __name__ == "__main__":
    g = Game()

g.show_start_screen()

while g.running:
    g.new()

pg.quit()

