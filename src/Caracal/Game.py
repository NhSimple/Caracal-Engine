from threading import Thread
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
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
        self.before_update.append(lambda: self.pygame.display.get_surface().blit(Object.sprite, (Object.x, Object.y)))
        self.before_update.append(Object.update)
        self.during_input.append(Object.input_update)
    
    def initialize_scene(self, Scene):
        for tile in Scene.tiles:
            self.surface.blit(tile[0],(tile[1],tile[2]))
        Scene.tiles.clear()
        Scene.calculate()

        self.Scene=Scene
                            #(texture, x-axis, y-axis.)
        

    def run(self):
        Thread(target=self.run_func).start()

    def run_func(self):
        pygame = self.pygame
        self.surface = self.window.set_mode((self.x,self.y))
        self.window.set_caption(self.window_name)
        logger.info("Pygame thread started.")
        while True:
            self.preflip_tasks()
            pygame.display.flip()
            self.surface.fill((0, 0, 0))

            self.inputs = pygame.event.get()
            pressed = pygame.key.get_pressed()
            if self.Scene is not None:
                self.initialize_scene(self.Scene)
            for input in self.inputs:
                if self.Scene is not None:
                    self.Scene.movement_control(pressed)
                self.input_tasks()
                
                if input.type == pygame.QUIT:
                    return
            



