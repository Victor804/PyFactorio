import pygame.locals
from core.map import Map, MapRenderer
from core.config import Config
import multiprocessing

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = GenerateMapScene(game)
        
    def handle_events(self):
        self.current_scene.handle_events()

    def update(self):
        self.current_scene.update()

    def render(self, screen):
        self.current_scene.render(screen)


class GenerateMapScene:
    def __init__(self, game):
        self.game = game
        self.map = None
        self.is_generating = True

        self.queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=self.generate_map, args=(self.queue,))
        self.process.start()

    def generate_map(self, queue):
        generated_map = Map()
        queue.put(generated_map)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        if self.is_generating and not self.queue.empty():
            self.map = self.queue.get()
            self.is_generating = False
            self.game.scene_manager.current_scene = MainScene(self.game, self.map)

    def render(self, screen):
        screen.fill((0, 0, 0))
        if self.is_generating:
            font = pygame.font.Font(None, 36)
            text = font.render("Generating Map...", True, (255, 255, 255))
            screen.blit(text, (50, 50))
        else:
            font = pygame.font.Font(None, 36)
            text = font.render("Map Generated! Transitioning...", True, (0, 255, 0))
            screen.blit(text, (50, 50))


class MainScene:
    def __init__(self, game, generated_map=None):
        self.game = game
        self.map_renderer = MapRenderer(generated_map if generated_map else Map(), Config.TILES_SIZE)

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

        self.map_renderer.set_mouse_pos(*pygame.mouse.get_pos())

    def update(self):
        pass

    def render(self, screen):
        self.map_renderer.render(screen)
        self.map_renderer.render_mouse(screen)