from threading import Thread
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
from functools import lru_cache

class Game:
    def __init__(self, window_name="Caracal Window", width=400, height=640):
        import pygame
        self.pygame = pygame
        self.window = pygame.display
        self.window_name = window_name
        self.SC_WIDTH = width
        self.SC_HEIGHT = height
        self.before_update=[]
        self.after_update=[]
        self.during_input=[]
        self.inputs=[]
        self.screen = None
        self.surface = pygame.Surface((width, height))
        self.Scene = None
        self.clock = pygame.time.Clock()
        self.max_fps = 0
        self._lazy_loads = []

    def preflip_tasks(self):
        #accepts functions as tasks to be handled BEFORE updating frames, in a list.
        for task in self.before_update:
            task()
    
    def postflip_tasks(self):
        #accepts functions as tasks to be handled AFTER updating frames, in a list.
        for task in self.after_update:
            task()

    def input_tasks(self):
        #accepts functions as tasks to be handled DURING the pygame event loop.
        for task in self.during_input:
            task()

    def instantiate(self, Object):
        self.before_update.append(lambda: self.screen.blit(Object.sprite, (Object.x, Object.y)))
        self.before_update.append(Object.update)
        self.during_input.append(Object.input_update)

    def _init_window(self):
        logger.info("Initializing window...")
        self.screen = self.window.set_mode((self.SC_WIDTH,self.SC_HEIGHT))
        self.after_update.append(lambda: self.window.set_caption(f"{self.window_name} - FPS: {self.fps:.2f} - dt: {self.dt:.2f}"))
        logger.info(f"Starting Load Tasks...")
        for task in self._lazy_loads:
            task[0](*task[1:])

    @lru_cache
    def initialize_scene(self, Scene):
        Scene.tiles.clear()
        Scene.calculate()
        self.Scene = Scene
        self.before_update.append(lambda: self.screen.blit(self.surface, (Scene.camera_x, Scene.camera_y)))
        for tile, iso_x, iso_y in self.Scene.tiles:
            x = self.Scene.camera_x + iso_x
            y = self.Scene.camera_y + iso_y
            self.surface.blit(Scene.texture[tile], (x, y))

    def run(self):
        Thread(target=self.run_func).start()

    def run_func(self):
        pygame = self.pygame
        self._init_window()
        self.window.set_caption(self.window_name)
        logger.info("Pygame thread started.")
        if self.Scene is not None:
            self.initialize_scene(self.Scene)
            self.draw_scene(self.Scene)
        logger.info("Ok")
        while True:
            self.screen.fill((0,0,0))
            self.preflip_tasks()
            self.dt = self.clock.tick(self.max_fps)
            self.fps = self.clock.get_fps()
            pygame.display.update()

            self.inputs = pygame.event.get()
            pressed = pygame.key.get_pressed()

            for input in self.inputs:
                if self.Scene is not None:
                    self.Scene.movement_control(pressed)
                else:
                    pass
                self.input_tasks()
                
                if input.type == pygame.QUIT:
                    return
                if input.type == pygame.KEYDOWN:
                    if input.key == pygame.K_F1:
                        self.Scene = self.initialize_scene(self.Scene)
                        self.draw_scene(self.Scene)
            
            self.postflip_tasks()  # not sure if this is the currect place for this 

