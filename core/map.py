import random
import numpy as np
from core.config import Config
import pygame

from enum import Enum

class TerrainType(Enum):
    EMPTY = 0
    ORE = 1
    GRASS = 2
    WATER = 3

class Map:
    def __init__(self):        
        self.map = np.zeros((Config.MAP_SIZE, Config.MAP_SIZE))
        self.generate_feature(TerrainType.ORE.value, num_features=500, feature_size=50, seed=42)

    def generate_feature(self, feature_type, num_features, feature_size, seed=0):
        random.seed(seed)
        for _ in range(num_features):
            start_x = random.randint(0, Config.MAP_SIZE - 1)
            start_y = random.randint(0, Config.MAP_SIZE - 1)
            
            for _ in range(feature_size):
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
                 TerrainType.ORE: (139, 69, 19),#BROWN
                 TerrainType.GRASS: (0, 128, 0),#GREEN
                 TerrainType.WATER: (0, 0, 255)#BLUE
                }

    
    def __init__(self, game_map, tile_size):
        """
        Initializes the MapRenderer.

        Args:
            game_map (numpy.ndarray): The 2D array representing the map.
            tile_size (int): Size of each tile in pixels.
            camera_width (int): Number of tiles the camera displays horizontally.
            camera_height (int): Number of tiles the camera displays vertically.
        """
        self.game_map = game_map
        self.tile_size = tile_size
        self.camera_width = Config.WINDOW_SIZE[0]//tile_size
        self.camera_height = Config.WINDOW_SIZE[1]//tile_size
        self.camera_x = 0
        self.camera_y = 0
        
        # Pre-render static map layer
        self.static_surface = pygame.Surface((game_map.map.shape[1] * tile_size, game_map.map.shape[0] * tile_size))
        self.static_surface.fill((0, 0, 0))
        self.render_static_map()
        

    def move_camera(self, dx, dy):
        """
        Moves the camera by the specified amount.

        Args:
            dx (int): Change in x position (tiles).
            dy (int): Change in y position (tiles).
        """
        self.camera_x = max(0, min(self.camera_x + dx, self.game_map.map.shape[1] - self.camera_width))
        self.camera_y = max(0, min(self.camera_y + dy, self.game_map.map.shape[0] - self.camera_height))


    def render_static_map(self):
        """Pre-renders the static part of the map."""
        for y in range(self.game_map.map.shape[0]):
            for x in range(self.game_map.map.shape[1]):
                tile_value = self.game_map.map[y][x]
                color = self.COLOR_MAP.get(TerrainType(tile_value), (255, 255, 255))
                pygame.draw.rect(
                    self.static_surface,
                    color,
                    pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size),
                )

    def render(self, screen):
        """Renders the visible portion of the map."""
        view_rect = pygame.Rect(
            self.camera_x * self.tile_size,
            self.camera_y * self.tile_size,
            self.camera_width * self.tile_size,
            self.camera_height * self.tile_size,
        )
        screen.blit(self.static_surface, (0, 0), view_rect)