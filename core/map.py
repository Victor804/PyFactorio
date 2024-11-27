import random
import numpy as np
from config import Config

from enum import Enum

class TerrainType(Enum):
    EMPTY = 0
    ORE = 1
    GRASS = 2
    WATER = 3

class Map:
    def __init__(self):        
        self.map = np.zeros((Config.MAP_SIZE, Config.MAP_SIZE))
        self.generate_feature(TerrainType.ORE.value, num_features=2, feature_size=2, seed=42)

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