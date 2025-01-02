from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y


    @abstractmethod
    def render(self, camera, screen):
        pass