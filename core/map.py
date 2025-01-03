import random
import numpy as np
from core.config import Config
import pygame

from enum import Enum

class TerrainType(Enum):
    EMPTY = 0
    COAL = 1
    IRON = 2
    GRASS = 3
    WATER = 4

class Map:
    def __init__(self, filename=None, seed=0):
        random.seed(seed)
        
        if filename:
            self.load_map(filename)
        else:            
            self.map = np.zeros((Config.MAP_SIZE, Config.MAP_SIZE))
            self.generate_lake(num=10, max_size=30)
            self.generate_feature(TerrainType.COAL.value, num_features=5, feature_size=5)
            self.generate_feature(TerrainType.IRON.value, num_features=5, feature_size=5)
            
            self.map[self.map == TerrainType.EMPTY.value] = TerrainType.GRASS.value

    def generate_lake(self, num, max_size):
        """
        Generates lakes with random shapes on the map.

        Args:
            num (int): Number of lakes to generate.
            max_size (int): Maximum size of each lake (number of cells).
        """
        for _ in range(num):
            start_x = random.randint(0, self.map.shape[1] - 1)
            start_y = random.randint(0, self.map.shape[0] - 1)

            lake_cells = {(start_x, start_y)}

            while len(lake_cells) < max_size:
                current_x, current_y = random.choice(list(lake_cells))

                neighbor_x = current_x + random.choice([-1, 0, 1])
                neighbor_y = current_y + random.choice([-1, 0, 1])

                if 0 <= neighbor_x < self.map.shape[1] and 0 <= neighbor_y < self.map.shape[0]:
                    lake_cells.add((neighbor_x, neighbor_y))

            for x, y in lake_cells:
                self.map[y][x] = TerrainType.WATER.value


    def generate_feature(self, feature_type, num_features, feature_size):
        """
        Generates features on the map, avoiding lakes or other predefined terrains.

        Args:
            feature_type (int): The type of feature to place (e.g., TerrainType.ORE.value).
            num_features (int): Number of features to generate.
            feature_size (int): Approximate size of each feature in cells.
        """
        for _ in range(num_features):
            while True:
                start_x = random.randint(0, Config.MAP_SIZE - 1)
                start_y = random.randint(0, Config.MAP_SIZE - 1)
                if self.map[start_y][start_x] == TerrainType.EMPTY.value:
                    break

            for _ in range(feature_size):
                if self.map[start_y][start_x] == TerrainType.EMPTY.value:
                    self.map[start_y][start_x] = feature_type

                start_x = max(0, min(Config.MAP_SIZE - 1, start_x + random.choice([-1, 0, 1])))
                start_y = max(0, min(Config.MAP_SIZE - 1, start_y + random.choice([-1, 0, 1])))

    def save_map(self, filename):
        np.save(filename, self.map)

    def load_map(self, filename):
        self.map = np.load(filename)

    def is_walkable(self, x, y, shape):
        """
        Vérifie si une zone rectangulaire est traversable.

        Args:
            x (int): Coordonnée x sur la carte.
            y (int): Coordonnée y sur la carte.
            shape (tuple): (largeur, hauteur) de l'objet.

        Returns:
            bool: True si la zone est entièrement traversable, sinon False.
        """

        map_height, map_width = self.map.shape
        width, height = shape

        for dy in range(height +1):
            for dx in range(width +1):
                tile_x = x + dx
                tile_y = y + dy

                if not (0 <= tile_x < map_width and 0 <= tile_y < map_height):
                    return False

                if self.map[int(tile_y)][int(tile_x)] == TerrainType.WATER.value:
                    return False

        return True
    
            
class MapRenderer:
    COLOR_MAP = {TerrainType.EMPTY: (0, 0, 0),#BLACK
                 TerrainType.COAL: (25, 25, 25),#DARK GRAY
                 TerrainType.IRON: (200, 200, 200),# LIGHT GRAY
                 TerrainType.GRASS: (0, 128, 0),#GREEN
                 TerrainType.WATER: (0, 0, 255)#BLUE
                }
    
    COLOR_MOUSE = (255, 255, 0)

    
    def __init__(self, game_map, camera):
        """
        Initializes the MapRenderer.

        Args:
            game_map (numpy.ndarray): The 2D array representing the map.
            tile_size (int): Size of each tile in pixels.
            camera_width (int): Number of tiles the camera displays horizontally.
            camera_height (int): Number of tiles the camera displays vertically.
        """
        self.game_map = game_map
        self.camera = camera
        self.mouse_pos = (0, 0)
        
        self.grass_image = pygame.image.load(Config.PATH_IMAGES + "grass.png").convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (Config.TILES_SIZE, Config.TILES_SIZE))
        
        self.coal_image = pygame.image.load(Config.PATH_IMAGES + "coal.png").convert_alpha()
        self.coal_image = pygame.transform.scale(self.coal_image, (Config.TILES_SIZE, Config.TILES_SIZE))
        
        self.iron_image = pygame.image.load(Config.PATH_IMAGES + "iron.png").convert_alpha()
        self.iron_image = pygame.transform.scale(self.iron_image, (Config.TILES_SIZE, Config.TILES_SIZE))
        
        self.static_surface = pygame.Surface((game_map.map.shape[1] * Config.TILES_SIZE, game_map.map.shape[0] * Config.TILES_SIZE))
        self.static_surface.fill((0, 0, 0))
        self.render_static_map()

    def set_mouse_pos(self, x, y):
        self.mouse_pos = (x, y)

    def render_static_map(self):
        for y in range(self.game_map.map.shape[0]):
            for x in range(self.game_map.map.shape[1]):
                tile_value = self.game_map.map[y][x]
                if TerrainType(tile_value) == TerrainType.GRASS:
                    self.static_surface.blit(self.grass_image, (x * Config.TILES_SIZE, y * Config.TILES_SIZE))
                elif TerrainType(tile_value) == TerrainType.COAL:
                    self.static_surface.blit(self.coal_image, (x * Config.TILES_SIZE, y * Config.TILES_SIZE))
                elif TerrainType(tile_value) == TerrainType.IRON:
                    self.static_surface.blit(self.iron_image, (x * Config.TILES_SIZE, y * Config.TILES_SIZE))
                else:
                    color = self.COLOR_MAP.get(TerrainType(tile_value), (255, 255, 255))
                    pygame.draw.rect(
                        self.static_surface, color, pygame.Rect(x * Config.TILES_SIZE, y * Config.TILES_SIZE, Config.TILES_SIZE, Config.TILES_SIZE)
                    )

    def render_mouse(self, screen):
        pygame.draw.rect(
            screen,
            self.COLOR_MOUSE,
            pygame.Rect(self.mouse_pos[0]//Config.TILES_SIZE * Config.TILES_SIZE,
                        self.mouse_pos[1]//Config.TILES_SIZE * Config.TILES_SIZE, 
                        Config.TILES_SIZE, 
                        Config.TILES_SIZE))

    def render(self, screen):
        """Renders the visible portion of the map."""
        view_rect = pygame.Rect(
            self.camera.x * Config.TILES_SIZE,
            self.camera.y * Config.TILES_SIZE,
            self.camera.width * Config.TILES_SIZE,
            self.camera.height * Config.TILES_SIZE,
        )
        screen.blit(self.static_surface, (0, 0), view_rect)