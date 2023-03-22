from threading import Thread
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
from functools import lru_cache
class Game:
    def __init__(self, window_name="Caracal Window", x=400,y=640):
        import pygame
        self.pygame = pygame
        self.window = pygame.display
        self.window_name = window_name
        self.x = x
        self.y = y
        self.before_update=[]
        self.after_update=[]
        self.during_input=[]
        self.inputs=[]
        self.surface = None
        self.Scene = None
        self.clock = pygame.time.Clock()
        self.max_fps = 120
    

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
        self.before_update.append(lambda: self.window.blit(Object.sprite, (Object.x, Object.y)))
        self.before_update.append(Object.update)
        self.during_input.append(Object.input_update)

    def draw_scene(self, Scene):
        for tile in self.Scene.tiles:
                    self.surface.blit(tile[0], (self.Scene.camera_x+tile[1], self.Scene.camera_y+tile[2]))
    
    @lru_cache
    def initialize_scene(self, Scene):
        
        Scene.tiles.clear()
        Scene.calculate()
        for tile in Scene.tiles:
            tile[0] = self.pygame.image.load(tile[0])
        self.Scene = Scene

                            #(texture, x-axis, y-axis.)
        self.before_update.append(lambda: self.window.set_caption(f"{self.window_name} - FPS: {self.fps:.2f} - dt: {self.dt:.2f}"))

        print("in")

    def run(self):
        Thread(target=self.run_func).start()

    def run_func(self):
        pygame = self.pygame
        self.surface = self.window.set_mode((self.x,self.y))
        self.window.set_caption(self.window_name)
        logger.info("Pygame thread started.")
        while True:
            self.preflip_tasks()
            self.dt = self.clock.tick(self.max_fps)
            self.fps = self.clock.get_fps()
            pygame.display.update()
            self.surface.fill((0, 0, 0))

            
            self.inputs = pygame.event.get()
            pressed = pygame.key.get_pressed()

            if self.Scene is not None:
                #Run separately from input loop to avoid being called only on key press. surface.fill may overwrite scene unless user is quick.
                self.initialize_scene(self.Scene)
                self.draw_scene(self.Scene)
                

            for input in self.inputs:
                if self.Scene is not None:
                    self.Scene.movement_control(pressed)
                else:
                    print(type(self.Scene))
                self.input_tasks()
                
                if input.type == pygame.QUIT:
                    return
            



