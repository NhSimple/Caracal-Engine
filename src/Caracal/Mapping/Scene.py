import pygame
import typing

from Caracal.Mapping.chunkManager2 import ChunkManager
from src.Caracal.Entities.entitymanager import EntityManager


class ısometricScene:
    def __init__(self) -> None:
        self.chunkManager = ChunkManager()
        self.entityHandler = EntityManager()
        self.entitySurface = None
        self.mapSurface = None

    def draw(self):
        self.chunkManager.draw(self.mapSurface)
        self.entityHandler.draw(self.entitySurface)
