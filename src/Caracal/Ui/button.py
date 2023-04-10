class Button:
    def __init__(self, text, x=0, y=0, width=64, height=64, color=(128, 128, 128)):
        import Caracal.Ui.text as text_mod
        import pygame
        from threading import Thread
        self.Thread = Thread
        pygame.init()
        self.pygame = pygame
        self.rect = self.pygame.Rect(x, y, width, height)
        self.text = text_mod.Label(text)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.state = "UP"

    def mousepos(self): return self.pygame.mouse.get_pos()

    def lockbutton(self):
        while True:
            if self.pygame.mouse.get_pressed()[0]:
                self.state = "DOWN"
            else:
                break
        self.state = "UP"

    def inputhandler(self, pressed, key):
        if self.pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(self.mousepos()):
                if self.state != "DOWN":
                    self.on_click()
                    self.Thread(target=self.lockbutton).start()
            else:
                pass

    def on_click(self):
        pass
