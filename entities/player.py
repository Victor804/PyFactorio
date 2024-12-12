import pygame
from core.config import Config
from core.crafting import Recipe
from entities.entity import Entity, Inventory
from core.crafting import CraftingMenu
from entities.ore import CoalItem, IronItem
from entities.driller import DrillerItem


class Player(Entity):
    COLOR = (255, 255, 255)
    SHAPE = (1, 2)
    SPEED = 0.2
    INVENTORY_SIZE = (10, 10)
    def __init__(self, x, y):
        super().__init__(x, y)        

        self.speed = self.SPEED
        
        self.shape = self.SHAPE

        self.image = pygame.Surface((Config.TILES_SIZE * self.shape[0], Config.TILES_SIZE * self.shape[1]))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()

        self.inventory = Inventory(self.INVENTORY_SIZE)
        self.crafting = CraftingMenu(self.inventory)
        
        self.crafting.add_recipe(PlayerRecipe.TRUC)
        self.crafting.add_recipe(PlayerRecipe.MACHIN)

    def handle_input(self, events, game_map):
        keys = pygame.key.get_pressed()
        
        if not self.inventory.windows_open:
            if keys[pygame.K_q]:
                _x = self.x - self.speed
                if game_map.is_walkable(_x, self.y, self.shape):
                    self.x = _x
                    
            if keys[pygame.K_d]:
                _x = self.x + self.speed
                if game_map.is_walkable(_x, self.y, self.shape):
                    self.x = _x

            if keys[pygame.K_z]:
                _y = self.y - self.speed
                if game_map.is_walkable(self.x, _y, self.shape):
                    self.y = _y
                
            if keys[pygame.K_s]:
                _y = self.y + self.speed
                if game_map.is_walkable(self.x, _y, self.shape):
                    self.y = _y
                
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.inventory.windows_open = not self.inventory.windows_open
                    
                if event.key == pygame.K_c:
                    self.crafting.windows_open = not self.crafting.windows_open
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.crafting.handle_click(event.pos)
            
    def render(self, camera, screen):
        """
        Render the player on the screen, considering the camera offset.
        Args:
            screen: The pygame surface to render on.
        """
        offset_x, offset_y = camera.get_offset()

        screen_x = (self.x * Config.TILES_SIZE) - offset_x
        screen_y = (self.y * Config.TILES_SIZE) - offset_y

        self.rect.topleft = (screen_x, screen_y)
        screen.blit(self.image, self.rect)
        
        self.inventory.render(screen, Config.WINDOW_SIZE[0]//2, Config.WINDOW_SIZE[1]//2, pygame.font.Font(None, 14))
        self.crafting.render(screen, Config.WINDOW_SIZE[0]//2, Config.WINDOW_SIZE[1]//2)
        
        
class PlayerRecipe:
    TRUC = Recipe("Truc", {IronItem:1}, (DrillerItem, 1))
    MACHIN = Recipe("MACHIN", {CoalItem:2}, (DrillerItem, 1))