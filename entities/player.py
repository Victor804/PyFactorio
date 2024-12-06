import pygame
from core.config import Config

class Player:
    def __init__(self, x, y, camera):
        self.image = pygame.Surface((Config.TILES_SIZE, Config.TILES_SIZE * 2))
        self.image.fill((255, 255, 255))

        # Position sur la carte
        self.x = x
        self.y = y

        # Taille du rectangle pour le rendu
        self.rect = self.image.get_rect()

        self.speed = 0.3  # Vitesse en pixels par frame
        self.camera = camera

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.x = max(0, self.x - self.speed)
        if keys[pygame.K_d]:
            self.x = min(Config.MAP_SIZE - 1, self.x + self.speed)
        if keys[pygame.K_z]:
            self.y = max(0, self.y - self.speed)
        if keys[pygame.K_s]:
            self.y = min(Config.MAP_SIZE - 2, self.y + self.speed)

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
