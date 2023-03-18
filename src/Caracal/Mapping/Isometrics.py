


class IsometricScene:
    def __init__(self, map, tile_width, tile_height, texture):
        import os
        import pygame
        self.os = os
        self.pygame = pygame
        self.map = map
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_half_width = tile_width / 2
        self.tile_half_height = tile_height / 4
        self.tiles = []
        self.texture = texture
        
    


        self.calculate()

    def calculate(self):
        #method created to reduce the load on the initialization method.
        pygame = self.pygame
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                # Calculate the position of the tile in isometric coordinates
                iso_x = (col - row) * self.tile_half_width
                iso_y = (col + row) * self.tile_half_height
                # Save the position of the tile as a tuple
                self.tiles.append((pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load(self.texture[self.map[row][col]]),(self.tile_width,self.tile_height)), 0, 1), iso_x, iso_y, True))
                print(self.tiles)
            

      


