from Caracal.drawHandler import DrawHandler
from Caracal.updateHandler import UpdateHandler
from Caracal.windowHandler import WindowHandler
from Caracal.gameStates import GameStates
import pygame
import os
import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


class Game:
    def __init__(self, windowHandler: WindowHandler) -> None:
        self.windowHandler = windowHandler
        self.gameStates = GameStates
        self.max_fps = 120
        self.updateHandler = UpdateHandler(self.gameStates.ANY, self)
        self.drawHandler = DrawHandler(self.gameStates.ANY)

    def run(self):
        self.running = True
        while self.running:
            self.updateHandler.update()
            self.drawHandler.draw()
        pygame.quit()
        raise SystemExit

    def stop(self):
        self.running = False
