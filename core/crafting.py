import pygame
from core.config import Config

class Recipe:
    def __init__(self, name, ingredients, output):
        """Represents a crafting recipe.

        Args:
            name (str): Name of the crafted item.
            ingredients (dict): Required items and their amounts.
            output (tuple): Resulting item and quantity.
        """
        self.name = name
        self.ingredients = ingredients
        self.output = output


class CraftingMenu:
    def __init__(self, inventory):
        """Initializes the crafting menu.

        Args:
            inventory (Inventory): The player's inventory instance.
        """
class CraftingMenu:
    def __init__(self, inventory):
        self.inventory = inventory
        self.recipes = []
        self.selected_recipe = None
        self.windows_open = False
        self.recipe_cells = {}  # Initialisation correcte


        
    def add_recipe(self, recipe):
        """Adds a new recipe to the crafting menu.

        Args:
            recipe (Recipe): The recipe to add.
        """
        self.recipes.append(recipe)

    def can_craft(self, recipe):
        """Checks if a recipe can be crafted.

        Args:
            recipe (Recipe): The recipe to check.

        Returns:
            bool: True if crafting is possible, False otherwise.
        """
        for item, amount in recipe.ingredients.items():
            print(item)
            if self.inventory.get_item_count(item) < amount:
                return False
        return True

    def craft(self, recipe):
        """Attempts to craft an item if possible.

        Args:
            recipe (Recipe): The recipe to craft.

        Returns:
            bool: True if crafting succeeded, False otherwise.
        """
        if not self.can_craft(recipe):
            return False

        for item, amount in recipe.ingredients.items():
            self.inventory.remove_item(item, amount)

        output_item, output_amount = recipe.output
        self.inventory.add_item(output_item, output_amount)
        return True
    
    def handle_click(self, mouse_pos):
        """Handles mouse clicks on the crafting menu."""
        if not self.windows_open:
            return

        for (row_idx, col_idx), recipe_index in self.recipe_cells.items():
            cell_x = Config.WINDOW_SIZE[0]//2 + col_idx * Config.INVENTORY_CELL_SIZE - len(self.recipes) * Config.INVENTORY_CELL_SIZE // 2
            cell_y = Config.WINDOW_SIZE[1]//2 + row_idx * Config.INVENTORY_CELL_SIZE - len(self.recipes) * Config.INVENTORY_CELL_SIZE // 2

            cell_rect = pygame.Rect(
                cell_x, cell_y, Config.INVENTORY_CELL_SIZE, Config.INVENTORY_CELL_SIZE
            )
            if cell_rect.collidepoint(mouse_pos) and recipe_index < len(self.recipes):
                recipe = self.recipes[recipe_index]
                self.craft(recipe)
                break


    def render(self, screen, x, y):
        """Renders the crafting menu."""
        grid_size = 1
        while grid_size**2 < len(self.recipes):
            grid_size += 1

        if self.windows_open:
            recipe_index = 0
            self.recipe_cells.clear()

            for row_idx in range(grid_size):
                for col_idx in range(grid_size):
                    cell_x = x + col_idx * Config.INVENTORY_CELL_SIZE - grid_size * Config.INVENTORY_CELL_SIZE // 2
                    cell_y = y + row_idx * Config.INVENTORY_CELL_SIZE - grid_size * Config.INVENTORY_CELL_SIZE // 2

                    cell_rect = pygame.Rect(
                        cell_x, cell_y, Config.INVENTORY_CELL_SIZE, Config.INVENTORY_CELL_SIZE
                    )

                    if recipe_index < len(self.recipes):
                        recipe = self.recipes[recipe_index]
                        color = recipe.output[0].COLOR
                        self.recipe_cells[(row_idx, col_idx)] = recipe_index
                    else:
                        color = (100, 100, 100)

                    if cell_rect.collidepoint(pygame.mouse.get_pos()):
                        color = (200, 200, 50)

                    pygame.draw.rect(screen, color, cell_rect)
                    pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)
                    
                    recipe_index += 1

