
import pygame as pg
import random
from settings import *
from abilities import AbilityCirclerAttack
vec = pg.math.Vector2

class AbilityChoice:
    """Template for an ability option on the level-up screen"""
    def __init__(self, ability_class, name, description, color):
        self.ability_class = ability_class
        self.name = name
        self.description = description
        self.color = color
        self.rect = None  # Will be set when drawing

class LevelUpScreen: # huge help from copilot auto agent built into VScode
    def __init__(self, game):
        self.game = game
        self.selected_abilities = []  # 3 random abilities
        self.choice_rects = []  # 3 rectangles for clicking
        
        # Define all available abilities
        self.all_abilities = [
            AbilityChoice(AbilityCirclerAttack, "Circler Attack", "Spawn 3 orbiting projectiles\naround you", YELLOW),
        ]
        
    def select_random_abilities(self): # randomly select 3 abilities for display
        # For now, just use what we have (can expand as you add more abilities)
        self.selected_abilities = random.sample(self.all_abilities, min(3, len(self.all_abilities)))
        self.choice_rects = []
        
    def draw(self, screen): # draws the ability choices
        # Semi-transparent dark overlay
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw title
        font_title = pg.font.Font(pg.font.match_font('arial'), 48)
        title_text = font_title.render("Level Up!", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Calculate button dimensions
        button_width = 150
        button_height = 100
        spacing = 30
        total_width = (button_width * len(self.selected_abilities)) + (spacing * (len(self.selected_abilities) - 1))
        start_x = (WIDTH - total_width) // 2
        start_y = HEIGHT // 2
        
        # Draw ability choices
        font_name = pg.font.Font(pg.font.match_font('arial'), 16)
        font_desc = pg.font.Font(pg.font.match_font('arial'), 12)
        
        self.choice_rects = []
        for i, ability in enumerate(self.selected_abilities):
            x = start_x + i * (button_width + spacing)
            y = start_y
            
            rect = pg.Rect(x, y, button_width, button_height)
            self.choice_rects.append((rect, ability))
            
            # Draw button background
            pg.draw.rect(screen, ability.color, rect)
            pg.draw.rect(screen, WHITE, rect, 3)  # Border
            
            # Draw ability name
            name_text = font_name.render(ability.name, True, BLACK)
            name_rect = name_text.get_rect(center=(rect.centerx, rect.y + 20))
            screen.blit(name_text, name_rect)
            
            # Draw description
            for line_idx, line in enumerate(ability.description.split('\n')):
                desc_text = font_desc.render(line, True, BLACK)
                desc_rect = desc_text.get_rect(center=(rect.centerx, rect.y + 45 + line_idx * 15))
                screen.blit(desc_text, desc_rect)
        
    def handle_click(self, pos): # for when player clicks to select an ability
        for rect, ability in self.choice_rects:
            if rect.collidepoint(pos):
                # Apply the selected ability to the player
                ability.ability_class(self.game, self.game.player)
                break