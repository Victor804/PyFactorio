import pygame
from core.config import Config
from core.crafting import Recipe
from entities.entity import Entity
from core.crafting import CraftingMenu
from entities.ore import *
from entities.driller import DrillerItem
from core.window import Window, Table


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

        self.inventory = Inventory(20, 2)
        self.crafting = CraftingMenu(self.inventory)
        
        self.crafting.add_recipe(PlayerRecipe.STONE_FURNACE)
        self.crafting.add_recipe(PlayerRecipe.MACHIN)

    def handle_input(self, events, game_map):
        keys = pygame.key.get_pressed()
        
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
                    self.inventory.window.is_open = not self.inventory.window.is_open
                               
                if event.key == pygame.K_c:
                    self.crafting.windows_open = not self.crafting.windows_open
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.crafting.handle_click(event.pos)
                
            self.inventory.handle_event(event)
            
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
        
        self.inventory.render(screen)
        self.crafting.render(screen, Config.WINDOW_SIZE[0]//2, Config.WINDOW_SIZE[1]//2)
        
        
class PlayerRecipe:
    STONE_FURNACE = Recipe("STONE_FURNACE", {StoneItem:1}, (DrillerItem, 1))
    MACHIN = Recipe("MACHIN", {CoalItem:2}, (DrillerItem, 1))
    

class Inventory:
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 300
    CELL_WIDTH = 150
    CELL_HEIGHT = 30
    TITLE_BAR_HEIGHT = 30

    def __init__(self, rows, cols, title="Player Inventory"):
        """
        Initialise l'inventaire avec une capacité fixe.

        Args:
            rows (int): Nombre de lignes (objets uniques max).
            cols (int): Nombre de colonnes pour afficher les données.
            title (str): Titre de la fenêtre.
        """
        self.rows = rows
        self.cols = cols
        self.capacity = rows * cols
        self.items = {}  # Stockage sous forme {objet: quantité}
        self.window = Window(100, 100, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, title)
        self.table = Table(
            10, self.TITLE_BAR_HEIGHT + 10, self.WINDOW_WIDTH - 20, self.WINDOW_HEIGHT - self.TITLE_BAR_HEIGHT - 20,
            data=[], 
            column_widths=[self.CELL_WIDTH] * 2, 
            header=["Object", "Quantity"]
        )
        self.window.add_component(self.table)

    def add_item(self, item, quantity=1):
        """
        Ajoute un objet à l'inventaire.

        Args:
            item (str): Nom de l'objet.
            quantity (int): Quantité à ajouter.
        """
        current_count = sum(self.items.values())
        if current_count + quantity > self.capacity:
            print("Inventory full!")
            return

        if item in self.items:
            self.items[item] += quantity
        else:
            if current_count < self.capacity:
                self.items[item] = quantity
        self.update_table()
        
        
    def get_item_count(self, item):
        """
        Compte le nombre d'item

        Args:
            item (str): Nom de l'objet.            
        """
        if item not in self.items.keys():
            return 0
        else:            
            return self.items[item]

    def remove_item(self, item, quantity=1):
        """
        Retire un objet de l'inventaire.

        Args:
            item (str): Nom de l'objet.
            quantity (int): Quantité à retirer.
        """
        if item in self.items:
            self.items[item] -= quantity
            if self.items[item] <= 0:
                del self.items[item]
        self.update_table()

    def update_table(self):
        """Met à jour les données du tableau avec le contenu de l'inventaire."""
        self.table.data = [[item, quantity] for item, quantity in self.items.items()]

    def render(self, screen):
        """Affiche l'inventaire."""
        self.window.render(screen)

    def handle_event(self, event):
        """Gère les événements pour l'inventaire."""
        self.window.handle_event(event)
