import pygame
import time
from threading import Thread
from functools import lru_cache
import os
import coloredlogs
import logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class Game:
    """ 
    Must run at 60 fps or fixed update must be set to less than 60 times a second.
    this cannot be because if fps dips below 60 fps updates halt proper too.
    So you must make sure to keep the game performant.
    """

    def __init__(self, window_name="Caracal Window", width=400, height=640):
        self.window_name = window_name
        self.SC_WIDTH, self.SC_HEIGHT = (width, height)
        self.clock = pygame.time.Clock()
        self.screen = None
        self.Scene = None
        self.max_fps = 120  # 0
        self._lazy_loads = []
        self._last_update_time = time.time()
        self._define_tasks()
        self.state = None
        self.gamestateList = []

        if os.path.exists(".caracal"):
            pass
        else:
            logger.info("Creating missing .caracal directory...")
            os.mkdir(".caracal")

    def _define_tasks(self):
        self.draw_tasks = []
        self.update_tasks = []
        self.input_tasks = []

    def instantiate(self, Object, gamestate, under_scene=None, update_task=None, input_task=None):
        """
        usage: Game.instantiate(Object)

        Alternatively, you can choose to make they object a child of the scene.
        This makes it correspond its position to the scenes camera, essentiall
        it synchronizes the map tiles with the Objects.
        """
        if under_scene is not None:
            _task = lambda: self.screen.blit(
                Object.sprite, (-self.Scene.camera_x + Object.x, -self.Scene.camera_y + Object.y))
        else:
            _task = lambda: self.screen.blit(
                Object.sprite, (Object.x, Object.y))
        self.draw_tasks.append({"task": _task, "gamestate": gamestate})
        if update_task: self.update_tasks.append({"task": update_task, "gamestate":gamestate})
        if input_task: self.input_tasks.append({"task":input_task, "gamestate":gamestate})

    def _init_window(self, gamestate, FLAGS=None):
        logger.info("Initializing...")
        self.screen = pygame.display.set_mode((self.SC_WIDTH, self.SC_HEIGHT), flags=FLAGS)
        _task = lambda: pygame.display.set_caption(f"{self.window_name} - FPS: {self.fps:.2f} - dt: {self.dt:.2f}")
        self.update_tasks.append({"task":_task, "gamestate":gamestate})
        logger.info(f"Starting Load Tasks...")
        for task in self._lazy_loads:
            task[0](*task[1:])

    @lru_cache
    def initialize_scene(self, Scene):
        self.Scene = Scene
        _task = lambda: self.screen.blit(self.Scene.surface, (-self.Scene.camera_x, -self.Scene.camera_y))
        self.draw_tasks.append({"task":_task, "gamestate":gamestate})

    def initialize_text(self, text, gamestate):
        # given screen and not surface because it is supposed to be higher than scene in the hierarchy.
        _task = lambda: self.screen.blit(text.text, text.text_rect)
        self.ui_queue.append({"task":_task, "gamestate":gamestate})

    def initialize_button(self, button):
        self.ui_queue.append(
            lambda: pygame.draw.rect(
                self.screen, button.color, button.rect)
        )
        self.during_input.append(
            lambda x: button.inputhandler(self.pressed, pygame))
        self.initialize_text(button.text)

    # @lru_cache
    def draw_scene(self, camera):
        # parameters: camera added so that the lru cache can update when these values update.
        if self.Scene is None:
            self.Scene.cache_surface()
        self.screen.fill("black")
        self.screen.blit(self.Scene.surface, (-camera.x, -camera.y))

    def run(self):
        Thread(target=self.run_func).start()

    def run_func(self):  # TODO: simplify and clean up this function.
        logger.info("Pygame thread started. OK.")
        while True:
            self.dt = self.clock.tick(self.max_fps)
            self.fps = self.clock.get_fps()
            
            self.preflip_tasks()
            self.draw_scene(self.Scene.camera)
            self.ui_tasks()
            pygame.display.update()
            self.pressed = pygame.key.get_pressed()

            current_time = time.time()
            elapsed_time = current_time - self._last_update_time
            # seperate input checks, otherwise you will have to time the window exit.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        # will be useful soon
                        pass

            if elapsed_time > 0.017:
                if self.Scene is not None:
                    self.Scene.movement_control(self.pressed, pygame)

                self.input_tasks(self.pressed, pygame)
                # seperate conditional statements as you dont want to update the scene every key press.

                self._last_update_time = time.time()

            self.postflip_tasks()  # not sure if this is the currect place for this

    def run_func(self):
        logger.info("Pygame thread started. OK.")
        while True:
            self.input()
            self.update()
            self.dt = self.clock.tick(self.max_fps)
            self.dt /= 1000  # convert to seconds
            self.draw()
    
    def draw(self):
        for data in self.draw_tasks:
            state_to_draw = data["state"]
            _task = data["task"]
            if self.state == state_to_draw:
                _task()
    
    def update(self):
        pass

    def input(self):
        pass