import pygame
import os
import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


from src.Caracal.gamestates import GameStates
from src.Caracal.windowhandler import WindowHandler
from src.Caracal.updatehandler import UpdateHandler
from src.Caracal.drawhandler import DrawHandler


# TODO: Add Scene


class Game:
    def __init__(self) -> None:
        self.windowHandler = WindowHandler()
        self.gameStates = GameStates()
        self.clock = pygame.time.Clock()
        self.max_fps = 120  # 0
        self.updateHandler = UpdateHandler(self.gameStates.ANY)
        self.drawHandler = DrawHandler(self.gameStates.ANY)

    def run(self):
        self.running = True
        while self.running:
            self.updateHandler.update()
            self.drawHandler.draw()
            self.dt = self.clock.tick(self.max_fps)

    def stop(self):
        self.running = False
