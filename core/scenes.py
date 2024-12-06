import pygame.locals
from core.map import Map, MapRenderer
from core.config import Config
from core.camera import Camera, CameraMode
from entities.player import Player
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
        
        self.camera = Camera(0, 0, Config.TILES_SIZE)
        self.player = Player(100, 100, self.camera)
                
        self.map_renderer = MapRenderer(generated_map, self.camera)
        pygame.mouse.set_visible(False)
        

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    if self.camera.mode is CameraMode.FREE:
                        self.camera.set_mode(CameraMode.TRACKING, self.player)
                        print("Track player")
                    else:
                        self.camera.set_mode(CameraMode.FREE)
                        print("Free")

                
        self.player.handle_input()

        self.camera.handle_input()
        self.map_renderer.set_mouse_pos(*pygame.mouse.get_pos())

    def update(self):
        self.camera.update()

    def render(self, screen):
        self.map_renderer.render(screen)
        
        self.player.render(screen)
        self.map_renderer.render_mouse(screen)