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
            self.generate_lake(num=100, max_size=200)
            self.generate_feature(TerrainType.COAL.value, num_features=500, feature_size=50)
            self.generate_feature(TerrainType.IRON.value, num_features=500, feature_size=50)
            
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

    def render_to_console(self):
        for row in self.map:
            print("".join(str(int(cell)) for cell in row))
            
            
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
        
        # Pre-render static map layer
        self.static_surface = pygame.Surface((game_map.map.shape[1] * Config.TILES_SIZE, game_map.map.shape[0] * Config.TILES_SIZE))
        self.static_surface.fill((0, 0, 0))
        self.render_static_map()
        

    def set_mouse_pos(self, x, y):
        self.mouse_pos = (x, y)

    def render_static_map(self):
        """Pre-renders the static part of the map."""
        for y in range(self.game_map.map.shape[0]):
            for x in range(self.game_map.map.shape[1]):
                tile_value = self.game_map.map[y][x]
                color = self.COLOR_MAP.get(TerrainType(tile_value), (255, 255, 255))
                pygame.draw.rect(
                    self.static_surface,
                    color,
                    pygame.Rect(x * Config.TILES_SIZE, y * Config.TILES_SIZE, Config.TILES_SIZE, Config.TILES_SIZE),
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