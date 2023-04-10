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
        self.camera_x = 0
        self.camera_y = 0
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

    def movement_control(self, pressed, key):
        if pressed[key.K_w]:
            self.camera_y += 10
        if pressed[key.K_s]:
            self.camera_y -= 10
        if pressed[key.K_a]:
            self.camera_x += 10
        if pressed[key.K_d]:
            self.camera_x -= 10

    def calculate(self):  # TODO: There shouldnt be both self.tiles and self.map, there should only be one
        # method created to reduce the load on the initiaization method.
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                # Calculate the position of the tile in isometric coordinates

                iso_x = (col - row) * self.tile_half_width / 2
                iso_y = (col + row) * self.tile_half_height / 4
                iso_x -= self.tile_half_width

                # Save the position of the tile as a tuple
                # maybe only save just the tile, not the iso pos?
                self.tiles.append([self.map[row][col], iso_x, iso_y])

    def get_mouse_pos(self):
        pygame = self.pygame
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # TODO: This should take the camera into account
        # BUG: Since the Isometric Rendering is from the topleft of an tile,
        # the camera doesn't seem fully be in the center of the scene, the half width of tile affects the Isometric Rendering
        # This function is correct, but we should fix rendering for it to work properly
        iso_x = (mouse_x / self.tile_half_width +
                 mouse_y / self.tile_half_height)
        iso_y = ((mouse_y / self.tile_half_height) -
                 (mouse_x / self.tile_half_width / 2)) / 2
        # iso_x = (mouse_x / self.tile_half_width + mouse_y / self.tile_half_height)
        # iso_y = (mouse_y / self.tile_half_height - (mouse_x / self.tile_half_width)) / 2

        iso_x = round(iso_x)
        iso_y = round(iso_y * 3)  # multiplying by 3 is important
        # I'm not sure if this is correct, but it seems to work

        return iso_x, iso_y
