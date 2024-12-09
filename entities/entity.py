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
        
        self.windows_open = False
        
    def add_item(self, x, y, item)->bool:
        """

        Args:
            x (int): x postion in cells
            y (int): y postion in cells
            item (Item): item you want to add

        Returns:
            bool: True if item add in inventory else False
        """
        assert 0 <= x < self.size[0] and 0 <= y < self.size[1]
        if self.cells[x][y].type == None:
            self.cells[x][y].type = item.name
            self.cells[x][y].add(1)
            return True
        
        elif self.cells[x][y].type == item.name:
            self.cells[x][y].add(1)
            return True       
        return False
        
    def render(self, screen, x, y, font):
        """
        Displays the inventory grid on the screen with items and quantities.

        Args:
            screen (pygame.Surface): The game screen where the inventory will be rendered.
            x (int): The x-coordinate of the top-left corner of the inventory.
            y (int): The y-coordinate of the top-left corner of the inventory.
            font (pygame.font.Font): The font used to display item information.
        """
        if self.windows_open:        
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
    def __init__(self, x, y):
        self.x = x
        self.y = y


    @abstractmethod
    def render(self, camera, screen):
        pass