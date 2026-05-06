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
from powerups import *
from abilities import *
import random
vec = pg.math.Vector2
from levelup_screen import *

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
        self.mob_spawn_cooldown = Cooldown(MOB_SPAWN_COOLDOWN_INITIAL)
        self.powerup_spawn_cooldown = Cooldown(POWERUP_INTERVAL)
        self.elapsed_time = 0  # track total game time 
        self.last_difficulty_increase = 0  # track last time difficulty increased
        self.camera = vec(0, 0) # camera position (top-left corner of the camera view)
        self.level_up_screen = LevelUpScreen(self)
        self.showing_levelup = False # level up screen isn't being displayed as of now

# a method is a function tied to a Class
    def load_data(self): # gets the map from the level1.txt file and makes all the wall have the designated sprite
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.wall_img = pg.image.load(path.join(self.img_dir, 'wall.png')).convert_alpha()
        self.map = Map(path.join(self.game_dir, 'level1.txt'))

    def new(self):
        self.load_data()

        # making all sprite, walls, mobs, etc. sprite groups
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.the_player = pg.sprite.Group()
        self.all_shockwaves = pg.sprite.Group()
        self.all_experience = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_forcefields = pg.sprite.Group()
        
        self.mob_spawn_cooldown.start() # starts the cooldown for mob spawning

        # loop to draw tiles on screen based on txt file (mostly walls + the player's starting position)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    # call class constructor without assigning a variable
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.run()

        
    # makes sure other methods occur while the program is running
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 # the passing of time in the proper tickrate
            self.events()
            if not self.paused: # pauses the updating of the game's elements when it is paused
                self.update()
            self.draw()

    def events(self):
        # stuff that happens with "peripherals" - keyboard, mouse
        for event in pg.event.get():
            # ends the game when it needs to be quit
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False 
                self.running = False
            
            # if event.type == pg.MOUSEBUTTONUP:
            #    print("I can get mouse input.")
            #    print(event.pos) # prints mouse's current coordinate
            # if event.type == pg.KEYUP:
            #     if event.key == pg.K_k:
            #         print("I can print when the K key is pressed.")
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_k:
            #         print("I can print when the K key is down.")

            # projectile firing
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: # ensuring that the mouse is left clicked
                    if self.player.fire_cooldown.ready():  # fire only if player's cooldown is ready
                        Projectile(self, self.player.pos.x, self.player.pos.y)
                        self.player.fire_cooldown.start() # restart cooldown for future projectiles

            # pausing the game when the 'p' key is pressed
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

            if self.showing_levelup:
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.level_up_screen.handle_click(event.pos)
                    self.showing_levelup = False
                    self.paused = False  # Unpause the game after ability selection
                        


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

    def mob_spawning(self):
        # spawns mobs in a method to avoid killing the old mob because of overlap
        if self.mob_spawn_cooldown.ready():  # spawn only if spawn cooldown has been reached
            candidate_spawn_pos = (random.randint(0, self.map.tilewidth - 1), random.randint(0, self.map.tileheight - 1))
            spawn_x = candidate_spawn_pos[0] * TILESIZE
            spawn_y = candidate_spawn_pos[1] * TILESIZE
            candidate = pg.sprite.Sprite()
            candidate.rect = pg.Rect(0, 0, TILESIZE, TILESIZE)
            candidate.rect.center = (spawn_x + TILESIZE / 2, spawn_y + TILESIZE / 2)
            candidate.hit_rect = candidate.rect.copy()

            hits = pg.sprite.spritecollide(candidate, self.all_shockwaves or self.all_walls, False, collide_hit_rect)
            if not hits:
                Mob(self, candidate_spawn_pos[0], candidate_spawn_pos[1])
                self.mob_spawn_cooldown.start()

    def spawn_powerups(self):
        if self.powerup_spawn_cooldown.ready():  # spawn only if powerup spawn cooldown has been reached
            candidate_pup_spawn_pos = (random.randint(0, self.map.tilewidth - 1), random.randint(0, self.map.tileheight - 1))
            spawn_x = candidate_pup_spawn_pos[0] * TILESIZE
            spawn_y = candidate_pup_spawn_pos[1] * TILESIZE
            candidate_pup = pg.sprite.Sprite()
            candidate_pup.rect = pg.Rect(0, 0, TILESIZE, TILESIZE)
            candidate_pup.rect.center = (spawn_x + TILESIZE / 2, spawn_y + TILESIZE / 2)
            candidate_pup.hit_rect = candidate_pup.rect.copy()


            hits = pg.sprite.spritecollide(candidate_pup, self.all_walls, False, collide_hit_rect)
            if not hits:
                choose_random_powerup(self, candidate_pup_spawn_pos[0], candidate_pup_spawn_pos[1])
                self.powerup_spawn_cooldown.start()

    def update(self):
        # self.player.rect.x += 1
        # if self.game_cooldown.ready():
        #     print("Cooldown done!")
        #     self.game_cooldown.start
        self.all_sprites.update()
        self.all_walls.update()
        self.all_mobs.update()
        #self.all_projectiles.update()
        
        # track elapsed time and increase difficulty (mob spawning, health, damage)
        self.elapsed_time += self.dt
        if self.elapsed_time - self.last_difficulty_increase >= DIFFICULTY_INTERVAL:
            self.last_difficulty_increase = self.elapsed_time

            new_cooldown = max(250, self.mob_spawn_cooldown.time - MOB_SPAWN_FREQUENCY_INCREASE)
            self.mob_spawn_cooldown.time = new_cooldown
            for mob in self.all_mobs: # goes through each mob in the mob group to apply damage and health increase
                mob.damage += 5
                mob.health += 20

        self.mob_spawning()
        self.spawn_powerups()

        # update camera to follow player
        self.update_camera()

        # ends game if the player loses all health (dies)
        if self.player.health <= 0:
            self.running = False

        # deals damage to mobs if they collide with the player's shockwave
        hits = pg.sprite.groupcollide(self.all_shockwaves, self.all_mobs, False, False, collide_hit_rect)
        for shockwave, mobs in hits.items():
            if shockwave.owner == self.player:
                for mob in mobs:
                    mob.health -= int(shockwave.damage * shockwave.owner.get_damage_multiplier())
        
        if self.player.level_up_flag:
            self.showing_levelup = True
            self.paused = True  # Pause the game during level-up
            self.level_up_screen.select_random_abilities()
            self.player.level_up_flag = False
    
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

        # draw health bar with camera offset and player position
        draw_health_bar(self.screen, self.player.pos.x - self.camera.x - BAR_LENGTH/2, self.player.pos.y - self.camera.y + BAR_HEIGHT*2, (self.player.health /self.player.max_health) * 100)
        draw_experience_bar(self.screen, self.player.pos.x - self.camera.x - BAR_LENGTH/2, self.player.pos.y - self.camera.y + BAR_HEIGHT*2 + BAR_HEIGHT, self.player.experience_points, self.player.xp_needed)
        
        # UI text (these stay in fixed screen positions, so no camera offset)
        
        minutes_elapsed = int(self.elapsed_time // 60)
        seconds_elapsed = int(self.elapsed_time % 60)
        self.draw_text(f"{minutes_elapsed}:{seconds_elapsed:02d}", 24, WHITE, 36, 0) # draws text with making sure that the seconds always have double digits
        
        # Calculate and display score
        score = int(self.player.mobs_defeated * 10 + (self.player.mobs_defeated * self.elapsed_time))
        self.draw_text(f"Score: {score}", 24, WHITE, WIDTH - 150, 0)
        # self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        # self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/2)
        # self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)

        if self.showing_levelup:
            self.level_up_screen.draw(self.screen)

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

