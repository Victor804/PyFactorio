import pygame
from core.config import Config

class Player:
    def __init__(self, x, y, camera):
        # Position sur la carte
        self.x = x
        self.y = y
        
        self.shape = (1, 2)

        self.image = pygame.Surface((Config.TILES_SIZE * self.shape[0], Config.TILES_SIZE * self.shape[1]))
        self.image.fill((255, 255, 255))

        # Taille du rectangle pour le rendu
        self.rect = self.image.get_rect()

        self.speed = 0.2  # Vitesse en pixels par frame
        self.camera = camera

    def handle_input(self, game_map):
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
            
    def render(self, screen):
        """
        Render the player on the screen, considering the camera offset.
        Args:
            screen: The pygame surface to render on.
        """
        offset_x, offset_y = self.camera.get_offset()

        screen_x = (self.x * Config.TILES_SIZE) - offset_x
        screen_y = (self.y * Config.TILES_SIZE) - offset_y

        self.rect.topleft = (screen_x, screen_y)
        screen.blit(self.image, self.rect)
