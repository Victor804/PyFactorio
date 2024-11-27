import pygame
from core.config import Config
from core.scenes import SceneManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Config.WINDOW_SIZE)
        pygame.display.set_caption(Config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene_manager = SceneManager(self)

    def run(self):
        while self.running:
            self.scene_manager.handle_events()
            self.scene_manager.update()
            self.scene_manager.render(self.screen)
            pygame.display.flip()
            self.clock.tick(Config.FPS)
        
        pygame.quit()
