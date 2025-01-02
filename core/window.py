import pygame

class Window:
    def __init__(self, x, y, width, height, title="Window"):
        self.rect = pygame.Rect(x, y, width, height)
        self.title_bar_rect = pygame.Rect(x, y, width, 30)
        self.title = title
        self.components = []
        self.is_open = True
        self.close_button_rect = pygame.Rect(x + width - 30, y, 30, 30)
        self.dragging = False
        self.drag_offset = (0, 0)
        
        self.is_resizable = False
        self.resizing = False
        self.resize_border = 10
        self.resize_dir = None

    def add_component(self, component):
        self.components.append(component)

    def render(self, screen):
        if not self.is_open:
            return
        
        # Fond de la fenêtre
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Barre de titre
        pygame.draw.rect(screen, (40, 40, 40), self.title_bar_rect)
        font = pygame.font.Font(None, 36)
        title_surface = font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surface, (self.title_bar_rect.x + 10, self.title_bar_rect.y + 5))

        # Bouton de fermeture
        pygame.draw.rect(screen, (200, 50, 50), self.close_button_rect)
        close_text = font.render("X", True, (255, 255, 255))
        screen.blit(close_text, (self.close_button_rect.x + 7, self.close_button_rect.y + 2))

        # Affichage des composants
        for component in self.components:
            component.render(screen, self.rect)

    def handle_event(self, event):
        """Gère les événements de la fenêtre."""
        if not self.is_open:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.is_open = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif self.title_bar_rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_offset = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            elif self.is_on_border(event.pos):
                self.resizing = True
                self.resize_dir = self.get_resize_dir(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.resizing = False

        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.topleft = (event.pos[0] - self.drag_offset[0], event.pos[1] - self.drag_offset[1])
                self.title_bar_rect.topleft = self.rect.topleft
                self.close_button_rect.topleft = (self.rect.right - 30, self.rect.top)
            if self.resizing and self.is_resizable:
                self.resize(event.pos)
            self.update_cursor(event.pos)

        for component in self.components:
            component.handle_event(event)


    def is_on_border(self, pos):
        x, y = pos
        on_left = self.rect.left <= x <= self.rect.left + self.resize_border
        on_right = self.rect.right - self.resize_border <= x <= self.rect.right
        on_top = self.rect.top <= y <= self.rect.top + self.resize_border
        on_bottom = self.rect.bottom - self.resize_border <= y <= self.rect.bottom

        on_horizontal_edge = (on_left or on_right) and self.rect.top < y < self.rect.bottom
        on_vertical_edge = (on_top or on_bottom) and self.rect.left < x < self.rect.right

        return on_horizontal_edge or on_vertical_edge

    def get_resize_dir(self, pos):
        x, y = pos
        resize_dir = []
        if abs(x - self.rect.left) <= self.resize_border:
            resize_dir.append("left")
        if abs(x - self.rect.right) <= self.resize_border:
            resize_dir.append("right")
        if abs(y - self.rect.top) <= self.resize_border:
            resize_dir.append("top")
        if abs(y - self.rect.bottom) <= self.resize_border:
            resize_dir.append("bottom")
        return resize_dir

    def resize(self, pos):
        x, y = pos
        if "right" in self.resize_dir:
            self.rect.width = max(100, x - self.rect.x)
        if "bottom" in self.resize_dir:
            self.rect.height = max(100, y - self.rect.y)
        if "left" in self.resize_dir:
            new_width = self.rect.right - x
            if new_width >= 100:
                self.rect.width = new_width
                self.rect.x = x
        if "top" in self.resize_dir:
            new_height = self.rect.bottom - y
            if new_height >= 100:
                self.rect.height = new_height
                self.rect.y = y

        # Mettre à jour les positions des éléments liés
        self.title_bar_rect.width = self.rect.width
        self.title_bar_rect.topleft = self.rect.topleft
        self.close_button_rect.topleft = (self.rect.right - 30, self.rect.top)

    def update_cursor(self, pos):
        if self.title_bar_rect.collidepoint(pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.is_on_border(pos):
            resize_dir = self.get_resize_dir(pos)
            if ("top" in resize_dir and "left" in resize_dir) or ("bottom" in resize_dir and "right" in resize_dir) and self.is_resizable:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
            elif ("top" in resize_dir and "right" in resize_dir) or ("bottom" in resize_dir and "left" in resize_dir) and self.is_resizable:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
            elif "right" in resize_dir or "left" in resize_dir and self.is_resizable:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            elif "top" in resize_dir or "bottom" in resize_dir and self.is_resizable:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

import pygame

class Table:
    def __init__(self, x, y, width, height, data, column_widths, header=None):
        """
        Crée un tableau interactif.

        Args:
            x (int): Position X du tableau relative à la fenêtre.
            y (int): Position Y du tableau relative à la fenêtre.
            width (int): Largeur du tableau.
            height (int): Hauteur du tableau.
            data (list of lists): Données à afficher (chaque sous-liste est une ligne).
            column_widths (list of int): Largeur des colonnes.
            header (list of str): Titres des colonnes (facultatif).
        """
        self.relative_rect = pygame.Rect(x, y, width, height)
        self.data = data
        self.column_widths = column_widths
        self.header = header
        self.cell_height = 30  # Hauteur de chaque cellule
        self.scroll_offset = 0  # Décalage pour le défilement vertical
        self.font = pygame.font.Font(None, 24)
        self.scroll_speed = 10  # Vitesse de défilement

    def render(self, screen, window_rect):
        """Affiche le tableau."""
        # Calcul des coordonnées absolues en fonction de la fenêtre
        self.rect = self.relative_rect.move(window_rect.topleft)

        # Bordure et fond
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Coordonnée Y pour commencer à dessiner
        y_offset = self.rect.y - self.scroll_offset

        # Affiche l'en-tête (s'il existe)
        if self.header:
            for col_index, col_name in enumerate(self.header):
                x_offset = self.rect.x + sum(self.column_widths[:col_index])
                column_rect = pygame.Rect(x_offset, y_offset, self.column_widths[col_index], self.cell_height)
                pygame.draw.rect(screen, (150, 150, 150), column_rect)
                pygame.draw.rect(screen, (0, 0, 0), column_rect, 1)
                text_surface = self.font.render(col_name, True, (0, 0, 0))
                screen.blit(text_surface, text_surface.get_rect(center=column_rect.center))
            y_offset += self.cell_height

        # Affiche les lignes de données
        for row in self.data:
            for col_index, cell_value in enumerate(row):
                x_offset = self.rect.x + sum(self.column_widths[:col_index])
                column_rect = pygame.Rect(x_offset, y_offset, self.column_widths[col_index], self.cell_height)
                pygame.draw.rect(screen, (255, 255, 255), column_rect)
                pygame.draw.rect(screen, (0, 0, 0), column_rect, 1)
                text_surface = self.font.render(str(cell_value), True, (0, 0, 0))
                screen.blit(text_surface, text_surface.get_rect(center=column_rect.center))
            y_offset += self.cell_height

    def handle_event(self, event):
        """Gère les interactions avec le tableau."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
            elif event.button == 5:  # Scroll down
                max_scroll = max(0, len(self.data) * self.cell_height - self.relative_rect.height)
                self.scroll_offset = min(max_scroll, self.scroll_offset + self.scroll_speed)
