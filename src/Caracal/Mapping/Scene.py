import pygame
import typing

from Caracal.Mapping.chunkManager2 import ChunkManager
from src.Caracal.Entities.entitymanager import EntityManager
from src.Caracal.game import Game


class IsometricScene:
    def __init__(self, app) -> None:
        self.app: Game = app
        self.chunkManager = ChunkManager()
        self.entityHandler = EntityManager()
        self.entitySurface = None

    def _init_surfaces(self):
        self.entitySurface = pygame.Surface(self.app.windowHandler.screenSize)

    def draw(self):
        self.chunkManager.draw(self.app.windowHandler.screen)
        self.entityHandler.draw(self.entitySurface)
