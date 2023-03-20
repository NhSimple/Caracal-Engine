import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

class GameObject:
    """    
    
    """
    def __init__(self, sprite,x=0,y=0):
        import pygame
        self.pygame = pygame
        self.x=x
        self.y=y
        try: 
            self.sprite = pygame.image.load(sprite)
        except Exception as e:
            logger.critical(f"Sprite cannot be loaded: {e}")
        
    

    def update(self):
        pass

    def input_update(self):
        pass

    def move(self, axis, distance):
        if axis == "x":
            self.x += distance
        elif axis =="y":
            self.y += distance
        else:
            raise ValueError("move only takes x and y as arguments.")

    def resize(self, x, y):
        self.sprite=self.pygame.transform.scale(self.sprite, (x,y))

        
    

