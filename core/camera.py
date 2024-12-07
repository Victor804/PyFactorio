from core.config import Config
from enum import Enum

import pygame

class CameraMode(Enum):
    FREE = 0
    TRACKING = 1

class Camera:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.width = Config.WINDOW_SIZE[0]//tile_size
        self.height = Config.WINDOW_SIZE[1]//tile_size

        self.mode = False
        self.entity = None
        
        
    def move_to(self, x, y):
        self.x = max(0, min(x, Config.MAP_SIZE - self.width))
        self.y = max(0, min(y, Config.MAP_SIZE - self.height))
        
        
    def move(self, dx, dy):
        self.x = max(0, min(self.x + dx, Config.MAP_SIZE - self.width))
        self.y = max(0, min(self.y + dy, Config.MAP_SIZE - self.height))


    def set_mode(self, mode, entity=None):
        self.mode = mode        
        self.entity = entity

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move(0, -0.2)
        if keys[pygame.K_DOWN]:
            self.move(0, 0.2)
        if keys[pygame.K_LEFT]:
            self.move(-0.2, 0)
        if keys[pygame.K_RIGHT]:
            self.move(0.2, 0)
            
    def update(self):
        if self.mode is CameraMode.TRACKING:
            if self.entity is not None:
                self.move_to(self.entity.x - self.width//2, self.entity.y - self.height//2)
                
                
    def get_offset(self):
        """
        Calculate the camera's offset for rendering.
        Returns:
            tuple: (offset_x, offset_y)
        """
        offset_x = self.x * Config.TILES_SIZE
        offset_y = self.y * Config.TILES_SIZE
        return offset_x, offset_y

        
        