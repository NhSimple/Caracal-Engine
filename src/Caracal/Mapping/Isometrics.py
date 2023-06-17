import typing
import pygame
from Caracal.Mapping.chunkManager2 import ChunkManager


class IsometricScene:
    def __init__(self, app, map, tile_width, tile_height, texture):
        self.app = app
        self.camera = pygame.math.Vector2(0, 0)
        self.map: typing.List[int, int, int] = map
        self.mapwidth, self.mapheight = (len(self.map), len(self.map[0]))
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_half_width = tile_width / 2
        self.tile_half_height = tile_height / 2
        self.tiles = []
        self.textures = texture
        self.updated = False
        self.surface = None
        self.chunkmanager = ChunkManager(
            self.app,
            self.textures,
            (self.mapwidth, self.mapheight),
            1,
            (self.tile_width, self.tile_height),
        )
        self._load_texture_lazy()

    def _load_texture_lazy(self, keep_alpha=True):
        if pygame.display.get_init():
            for i, tex_path in enumerate(self.textures):
                img = pygame.image.load(tex_path)
                img = img.convert_alpha() if keep_alpha else img.convert()
                self.textures[i] = img
        else:
            self.app._lazy_loads.append((self._load_texture_lazy, keep_alpha))

    def cache_surface(
        self,
    ):  # TODO: There shouldnt be both self.tiles and self.map, there should only be one
        self.surface = pygame.Surface(
            (self.mapwidth * self.tile_width, self.mapheight * 0.5 * self.tile_height)
        )
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                # Calculate the position of the tile in isometric coordinates
                iso_x = (col - row) * self.tile_half_width / 2
                iso_y = (col + row) * self.tile_half_height / 4
                iso_x -= self.tile_half_width

                # Save the position of the tile as a tuple
                # maybe only save just the tile, not the iso pos?
                self.tiles.append([self.map[row][col], iso_x, iso_y])

        for tile, iso_x, iso_y in self.tiles:
            width, height = self.surface.get_size()
            x = (
                iso_x + width / 2
            )  # WARNING: TODO: This could cause problems with the mouse pos to isopos converted
            y = iso_y
            self.surface.blit(self.textures[tile], (x, y))

    def get_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # TODO: This should take the camera into account
        iso_x = mouse_x / self.tile_half_width + mouse_y / self.tile_half_height
        iso_y = (
            (mouse_y / self.tile_half_height) - (mouse_x / self.tile_half_width / 2)
        ) / 2
        # iso_x = (mouse_x / self.tile_half_width + mouse_y / self.tile_half_height)
        # iso_y = (mouse_y / self.tile_half_height - (mouse_x / self.tile_half_width)) / 2

        iso_x = round(iso_x)
        iso_y = round(iso_y * 3)  # multiplying by 3 is important
        # I'm not sure if this is correct, but it seems to work

        return iso_x, iso_y
