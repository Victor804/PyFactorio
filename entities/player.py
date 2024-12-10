import pygame
from core.config import Config
from entities.entity import Entity, Inventory

class Player(Entity):
    def __init__(self, x, y, shape):
        super().__init__(x, y, shape)        

        self.speed = 0.2

        self.inventory = Inventory((10, 10))
        self.inventory_open = False

    def handle_input(self, events, game_map):
        keys = pygame.key.get_pressed()
        
        if not self.inventory_open:
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
                    self.inventory_open = not self.inventory_open
            
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
        
        if self.inventory_open:
            self.inventory.render(screen, Config.WINDOW_SIZE[0]//2, Config.WINDOW_SIZE[1]//2, pygame.font.Font(None, 36))
