import pygame.locals

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
        self.map

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
