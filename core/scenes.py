import pygame.locals
from core.map import Map, MapRenderer
from core.config import Config

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = MainScene(game)

    def handle_events(self):
        self.current_scene.handle_events()

    def update(self):
        self.current_scene.update()

    def render(self, screen):
        self.current_scene.render(screen)



class MainScene:
    def __init__(self, game):
        self.game = game
        self.map_renderer = MapRenderer(Map(), Config.TILES_SIZE)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.map_renderer.move_camera(0, -1)
        if keys[pygame.K_DOWN]:
            self.map_renderer.move_camera(0, 1)
        if keys[pygame.K_LEFT]:
            self.map_renderer.move_camera(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.map_renderer.move_camera(1, 0)


    def update(self):
        pass

    def render(self, screen):
        self.map_renderer.render(screen)
