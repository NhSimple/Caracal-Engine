import pygame
from src.Caracal.Entities.entity import Entity


class TestEntity(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.time = 0

    def update(self, dt):
        self.time += dt

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), (self.time, 0, 50, 50))
