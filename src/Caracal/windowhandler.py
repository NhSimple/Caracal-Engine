import pygame


class WindowHandler:
    def __init__(self, flags=0, size=(400, 640), name="Caracal Test Window") -> None:
        """Starts and manages the game window.

        Args:
            flags (int, optional): Display surface flags. Defaults to 0.
            size (tuple, optional): Screen size. Defaults to (400, 640).
            name (str, optional): Window name. Defaults to "Caracal Test Window".
        """
        self.flags = flags
        self.size = size
        self.name = name
        self.screen = None
        self._init_window()

    def _init_window(self):
        self.screen = pygame.display.set_mode(self.size, flags=self.flags)
        self.set_name(self.name)

    def set_name(self, name):
        self.name = name
        pygame.display.set_caption(self.name)
