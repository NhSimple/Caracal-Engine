class Label:
    def __init__(self, text, x=0, y=0, font="Arial", size=32, color=(255, 255, 255)):
        from pygame import font as font_mod
        font_mod.init()
        font = font_mod.SysFont("Arial", 32)
        self.text = font.render(text, True, (color))
        self.text_rect = self.text.get_rect()
        self.text_rect.x, self.text_rect.y = x, y

        self.text_rect.center = (self.text_rect.x, self.text_rect.y)
