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
        self.ui_queue = []
        self.before_update = []
        self.after_update = []
        self.during_input = []
        self.inputs = []
        self.screen = None
        self.Scene = None
        self.clock = pygame.time.Clock()
        self.max_fps = 120  # 0
        self._lazy_loads = []
        self._last_update_time = time.time()

        if os.path.exists(".caracal"):
            pass
        else:
            logger.info("Creating missing .caracal directory...")
            os.mkdir(".caracal")

    def preflip_tasks(self):
        # accepts functions as tasks to be handled BEFORE updating frames, in a list.
        for task in self.before_update:
            print(str(task))
            task()

    def postflip_tasks(self):
        # accepts functions as tasks to be handled AFTER updating frames, in a list.
        for task in self.after_update:
            task()

    def input_tasks(self, pressed, pygame):
        # accepts functions as tasks to be handled DURING the pygame event loop.
        for task in self.during_input:
            task(pressed)

    def ui_tasks(self):
        # accepts functions as tasks to be drawn LAST amongst all other blits and serves the purpose of interactable ui.
        for task in self.ui_queue:
            task()

    def instantiate(self, Object, under_scene=None):
        """
        usage: Game.instantiate(Object)

        Alternatively, you can choose to make the object a child of the scene.
        This makes it correspond its position to the scenes camera, essentially
        it synchronizes the map tiles with the Objects.
        """
        if under_scene is not None:
            self.before_update.append(lambda: self.screen.blit(
                Object.sprite, (-self.Scene.camera_x + Object.x, -self.Scene.camera_y + Object.y)))
            self.before_update.append(Object.update)
            self.during_input.append(Object.input_update)
        else:
            self.before_update.append(lambda: self.screen.blit(
                Object.sprite, (Object.x, Object.y)))
            self.before_update.append(Object.update)
            self.during_input.append(Object.input_update)

    def _init_window(self):
        logger.info("Initializing window...")
        self.screen = pygame.display.set_mode((self.SC_WIDTH, self.SC_HEIGHT))
        logger.info("Initializing ui...")
        self.after_update.append(lambda: pygame.display.set_caption(
            f"{self.window_name} - FPS: {self.fps:.2f} - dt: {self.dt:.2f}"))
        logger.info(f"Starting Load Tasks...")
        for task in self._lazy_loads:
            task[0](*task[1:])

    @lru_cache
    def initialize_scene(self, Scene):
        self.Scene = Scene
        # self.Scene.cache_surface()
        self.before_update.append(
            lambda: self.screen.blit(self.Scene.surface, (-self.Scene.camera_x, -self.Scene.camera_y)))

    def initialize_text(self, text):
        self.ui_queue.append(
            # given screen and not surface because it is supposed to be higher than scene in the hierarchy.
            lambda: self.screen.blit(text.text, text.text_rect))

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
        pygame.display.set_caption(self.window_name)
        logger.info("Pygame thread started.")
        logger.info("OK")
        while True:
            self.dt = self.clock.tick(self.max_fps)
            self.fps = self.clock.get_fps()
            
            self.preflip_tasks()
            self.draw_scene(self.Scene.camera)
            self.ui_tasks()
            pygame.display.update()

            self.inputs = pygame.event.get()
            self.pressed = pygame.key.get_pressed()

            current_time = time.time()
            elapsed_time = current_time - self._last_update_time
            # seperate input checks, otherwise you will have to time the window exit.
            for input in self.inputs:
                if input.type == pygame.QUIT:
                    return
                if input.type == pygame.KEYDOWN:
                    if input.key == pygame.K_F1:
                        # will be useful soon
                        pass

            if elapsed_time > 0.017:
                if self.Scene is not None:
                    self.Scene.movement_control(self.pressed, pygame)

                self.input_tasks(self.pressed, pygame)
                # seperate conditional statements as you dont want to update the scene every key press.

                self._last_update_time = time.time()

            self.postflip_tasks()  # not sure if this is the currect place for this
