import pygame
from abc import ABC, abstractmethod
from core.config import Config
import numpy as np

class InventoryCell:
    def __init__(self, object_type, count):
        self.type = object_type
        self.count = count
        
    def add(self, n):
        self.count += n
        
    def sub(self, n):
        assert self.count >= n
        self.count -= n
        
        if self.count == 0:
            self.type = None
            
    def __str__(self):
        return f"{self.type.NAME}:{self.count}"
        
class Inventory:
    def __init__(self, size, cell_size=Config.INVENTORY_CELL_SIZE):
        self.size = size
        self.cell_size = cell_size
        self.cells = [[InventoryCell(None, 0) for _ in range(size[0])] for _ in range(size[1])]
        self.selected_cell = (-1, -1)
        
        self.windows_open = False
        
    def find_item(self, item_type):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if cell.type == item_type and cell.count > 0:
                    return x, y
        return None
    
    def get_item_count(self, item_type):
        total = 0
        for row in self.cells:
            for cell in row:
                print(cell.type, item_type)
                if cell.type == item_type:
                    total += cell.count
        return total
        
    def add_item(self, item_type, count=1):
        for row in self.cells:
            for cell in row:
                if cell.type == item_type or cell.type is None:
                    space = Config.MAX_STACK_SIZE - cell.count
                    added = min(space, count)
                    cell.add(added)
                    cell.type = item_type
                    count -= added
                    if count <= 0:
                        return True
        return False
    
    def remove_item(self, item_type, count):
        for row in self.cells:
            for cell in row:
                if cell.type == item_type and cell.count > 0:
                    removed = min(cell.count, count)
                    cell.sub(removed)
                    count -= removed
                    if count <= 0:
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
                        text = font.render(f"{cell}", True, (255, 255, 255))
                        screen.blit(text, (cell_rect.x + 5, cell_rect.y + 5))


class Entity(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y


    @abstractmethod
    def render(self, camera, screen):
        pass