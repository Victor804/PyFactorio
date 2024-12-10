import pygame
from abc import ABC, abstractmethod
from core.config import Config
import numpy as np

class InventoryCell:
    def __init__(self, object_type, num):
        self.type = object_type
        self.num = num
        
    def add(self, n):
        self.num += n
        
    def sub(self, n):
        assert self.num >= n
        self.num -= n
        
        if self.num == 0:
            self.type = None
        
class Inventory:
    def __init__(self, size, cell_size=Config.INVENTORY_CELL_SIZE):
        self.size = size
        self.cell_size = cell_size
        self.cells = [[InventoryCell(None, 0) for _ in range(size[0])] for _ in range(size[1])]
        self.selected_cell = (-1, -1)
        
        
    def render(self, screen, x, y, font):
        """
        Displays the inventory grid on the screen with items and quantities.

        Args:
            screen (pygame.Surface): The game screen where the inventory will be rendered.
            x (int): The x-coordinate of the top-left corner of the inventory.
            y (int): The y-coordinate of the top-left corner of the inventory.
            font (pygame.font.Font): The font used to display item information.
        """
        for row_idx, row in enumerate(self.cells):
            for col_idx, cell in enumerate(row):
                cell_rect = pygame.Rect(
                    x + col_idx * self.cell_size - self.size[0] * self.cell_size //2,
                    y + row_idx * self.cell_size - self.size[1] * self.cell_size //2,
                    self.cell_size,
                    self.cell_size,
                )

                if cell_rect.collidepoint(pygame.mouse.get_pos()):
                    color = (200, 200, 50)
                    self.selected_cell = (row_idx, col_idx)
                else:
                    color = (100, 100, 100)

                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)

                if cell.type:
                    text = font.render(f"{cell.type}: {cell.num}", True, (255, 255, 255))
                    screen.blit(text, (cell_rect.x + 5, cell_rect.y + 5))


class Entity(ABC):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        
        self.shape = (1, 2)

        self.image = pygame.Surface((Config.TILES_SIZE * self.shape[0], Config.TILES_SIZE * self.shape[1]))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()


    @abstractmethod
    def render(self, camera, screen):
        pass