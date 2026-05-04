
import pygame as pg
import random
from settings import *
from abilities import *
vec = pg.math.Vector2

class AbilityChoice:
    def __init__(self, ability_class, name, description, color):
        self.ability_class = ability_class # the ability being chosen
        self.name = name
        self.description = description
        self.color = color
        self.rect = None  # will be set when drawing

class LevelUpScreen: # huge help from copilot auto agent built into VScode
    def __init__(self, game):
        self.game = game
        self.selected_abilities = []  # 3 random abilities
        self.choice_rects = []  # 3 rectangles for clicking
        
        # put all available abilities into a list for choosing
        self.all_abilities = [
            AbilityChoice(CirclerAttack, "Circler Attack", "Spawn 3 orbiting projectiles\naround you", YELLOW),
            AbilityChoice(Xp_Gain_Boost, "Xp Gain Boost", "Gain more experience from\nexperience orbs", LIGHT_BLUE),
            AbilityChoice(Max_Health_Boost, "Max Health Boost", "Higher max health", PURPLE),
            AbilityChoice(Health_Gain_Boost, "Health Gain Boost", "Recover health faster", DARK_RED),
            AbilityChoice(Forcefield, "Slowing Forcefield", "Slows down mobs in\nthe forcefield's range", PINK)
        ]
        
    def select_random_abilities(self): # randomly select 3 abilities for display
        self.selected_abilities = random.sample(self.all_abilities, min(3, len(self.all_abilities))) # selects an amount of the abilities out of all_abilities and stores them
        self.choice_rects = []
        
    def draw(self, screen): # draws the ability choices
        # semi-transparent dark overlay
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0)) # puts the overlay over the screen
        
        # draw message
        font_message = pg.font.Font(pg.font.match_font('arial'), )
        title_text = font_message.render("Choose Your Ability:", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # calculate button dimensions
        button_width = 150
        button_height = 100
        spacing = 30
        total_width = (button_width * len(self.selected_abilities)) + (spacing * (len(self.selected_abilities) - 1))
        start_x = (WIDTH - total_width) // 2
        start_y = HEIGHT // 2
        
        # draw ability choices
        font_name = pg.font.Font(pg.font.match_font('arial'), 16)
        font_desc = pg.font.Font(pg.font.match_font('arial'), 12)
        
        self.choice_rects = []
        for i, ability in enumerate(self.selected_abilities):
            x = start_x + i * (button_width + spacing) # draws next box based on previous boxes drawn so that they are evenly on the screen
            y = start_y
            
            rect = pg.Rect(x, y, button_width, button_height)
            self.choice_rects.append((rect, ability)) # adds the already drawn rect to the list to keep track
            
            # draw button background
            pg.draw.rect(screen, ability.color, rect)
            pg.draw.rect(screen, WHITE, rect, 3)  # Border
            
            # draw ability name
            name_text = font_name.render(ability.name, True, BLACK)
            name_rect = name_text.get_rect(center=(rect.centerx, rect.y + 20))
            screen.blit(name_text, name_rect)
            
            # draw description
            for line_idx, line in enumerate(ability.description.split('\n')): # goes through each line in the description and separates them across lines
                desc_text = font_desc.render(line, True, BLACK)
                desc_rect = desc_text.get_rect(center=(rect.centerx, rect.y + 45 + line_idx * 15)) # leaves 15 pixels between lines and centers them
                screen.blit(desc_text, desc_rect)
        
    def handle_click(self, pos): # for when player clicks to select an ability
        for rect, ability in self.choice_rects:
            if rect.collidepoint(pos):
                ability.ability_class(self.game, self.game.player) # apply the selected ability to the player
                break