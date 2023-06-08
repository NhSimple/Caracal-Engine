import pygame
import os
import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


from Caracal.gameStates import GameStates
from Caracal.windowHandler import WindowHandler
from Caracal.updateHandler import UpdateHandler
from Caracal.drawHandler import DrawHandler



class Game:
    def __init__(self) -> None:
        self.windowHandler = WindowHandler(name="Caracal Test Window")
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
