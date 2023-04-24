class Button:
    def __init__(self, text, x=0, y=0, width=64, height=64, color=(128, 128, 128), text_size=1.5):
        import Caracal.Ui.text as text_mod
        import pygame
        from threading import Thread
        self.Thread = Thread
        pygame.init()
        self.pygame = pygame
        self.rect = self.pygame.Rect(x, y, width, height)
        self.text_size = text_size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text_mod.Label(text, x=self.x, y=self.y)
        self.text.text_rect.x = self.x
        self.text.text_rect.y = self.y
        self.text.text_rect.center = self.rect.center

        self.state = "UP"

        # make text size a fraction of the area.
        self.text.size = self.width*self.height
        print(self.text.size)

    def mousepos(self): return self.pygame.mouse.get_pos()

    def inputhandler(self, pressed, key):
        if self.pygame.mouse.get_pressed()[0] and self.state == "UP":
            if self.rect.collidepoint(self.mousepos()):
                if self.state != "DOWN":
                    self.on_click()
            else:
                pass
        # captures input frame by frame to see if being pressed or held.

        if self.pygame.mouse.get_pressed()[0]:
            self.state = "DOWN"
        else:
            self.state = "UP"

    def on_click(self):
        pass
