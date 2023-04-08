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
        self.max_fps = 60 # 0
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
        self.Scene = Scene
        self.before_update.append(lambda: self.screen.blit(self.surface, (0, 0)))
            
            
    @lru_cache
    def draw_scene(self, camera_x, camera_y):
        #parameters: camera_x, camera_y added so that the lru cache can update when these values update.
        Scene = self.Scene
        self.surface.fill((0,0,0))

        Scene.calculate()
        
        for tile, iso_x, iso_y in self.Scene.tiles:
            x = Scene.camera_x + iso_x
            y = Scene.camera_y + iso_y

            self.surface.blit(Scene.texture[tile], (x, y))   
        Scene.tiles.clear()
        


    def run(self):
        Thread(target=self.run_func).start()

    def run_func(self):
        pygame = self.pygame
        self._init_window()
        self.window.set_caption(self.window_name)
        logger.info("Pygame thread started.")

        logger.info("Ok")
        while True:
            
            self.preflip_tasks()
            self.dt = self.clock.tick(self.max_fps)
            self.fps = self.clock.get_fps()
            if self.Scene is not None:

                self.draw_scene(self.Scene.camera_x, self.Scene.camera_y)
                
            
            
            self.window.update()
            
            self.inputs = pygame.event.get()
            pressed = pygame.key.get_pressed()

                #seperate conditional statements as you dont want to update the scene every key press.
            for input in self.inputs:
                if self.Scene is not None:
                    self.Scene.movement_control(pressed)

                self.input_tasks()
                
                if input.type == pygame.QUIT:
                    return
                if input.type == pygame.KEYDOWN:
                    if input.key == pygame.K_F1:
                        #consider removing this function call unless its a debug thing.
                        self.draw_scene()
            
            
            self.postflip_tasks()  # not sure if this is the currect place for this 

