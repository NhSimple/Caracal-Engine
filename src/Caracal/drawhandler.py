import pygame


class DrawHandler:
    def __init__(self, state) -> None:
        self.draw_tasks = []
        self.ui_queue = []
        self.state = state

    def draw(self):
        for task in self.draw_tasks:
            _task = task["task"]
            gamestate = task["gamestate"]
            if gamestate == self.state:
                _task()
        for task in self.ui_queue:
            _task = task["task"]
            gamestate = task["gamestate"]
            if gamestate == self.state:
                _task()