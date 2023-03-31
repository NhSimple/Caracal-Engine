import typing


class IsometricScene:
    def __init__(self, app, map, tile_width, tile_height, texture):
        self.app = app
        import pygame
        self.pygame = pygame
        self.map: typing.List[int, int, int] = map
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_half_width = tile_width / 2
        self.tile_half_height = tile_height / 2
        self.tiles = []
        self.texture = texture
        self.camera_x=0
        self.camera_y=0
        self.updated = False
        self._load_texture_lazy()
        self.calculate()

    def _load_texture_lazy(self, keep_alpha=True):
        if self.pygame.display.get_init():
            for i, tex_path in enumerate(self.texture):
                img = self.pygame.image.load(tex_path)
                img = img.convert_alpha() if keep_alpha else img.convert()
                self.texture[i] = img
        else:
            self.app._lazy_loads.append((self._load_texture_lazy, keep_alpha))

    def movement_control(self, pressed):
        pygame = self.pygame
        if pressed[pygame.K_w]:
            self.camera_y += 10
        if pressed[pygame.K_s]:
            self.camera_y -= 10
        if pressed[pygame.K_a]:
            self.camera_x += 10
        if pressed[pygame.K_d]:
            self.camera_x -= 10

    def calculate(self):  # TODO: There shouldnt be both self.tiles and self.map, there should only be one
        #method created to reduce the load on the initialization method.
        pygame = self.pygame
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                # Calculate the position of the tile in isometric coordinates
                iso_x = (col - row) * self.tile_half_width/2
                iso_y = (col + row) * self.tile_half_height/4
                # Save the position of the tile as a tuple
                self.tiles.append([self.map[row][col], iso_x, iso_y])  # maybe only save just the tile, not the iso pos?