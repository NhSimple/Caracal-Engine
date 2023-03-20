


class IsometricScene:
    def __init__(self, map, tile_width, tile_height, texture):
        import pygame
        self.pygame = pygame
        self.map = map
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_half_width = tile_width / 2
        self.tile_half_height = tile_height / 2
        self.tiles = []
        self.texture = texture
        self.camera_x=0
        self.camera_y=0
            
        self.prepare_textures()

        self.calculate()


    def movement_control(self, pressed):
        pygame = self.pygame
        if pressed[pygame.K_w]:
            self.camera_y -= 10
        if pressed[pygame.K_s]:
            self.camera_y += 10
        if pressed[pygame.K_a]:
            self.camera_x += 10
        if pressed[pygame.K_d]:
            self.camera_x -= 10

    def prepare_textures(self):
        pygame = self.pygame
        current_texture = 0
        for tile in self.texture:
            self.texture[current_texture] = pygame.transform.scale(pygame.image.load(tile),(self.tile_width, self.tile_height))
            # if we go the shearing route, then rotation is likely unnecessary.
            current_texture += 1
            print(tile)

    def calculate(self):
        #method created to reduce the load on the initialization method.
        pygame = self.pygame
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                print(self.texture)
                # Calculate the position of the tile in isometric coordinates
                iso_x = (col - row) * self.tile_half_width
                iso_y = (col + row) * self.tile_half_height/4
                # Save the position of the tile as a tuple
                self.tiles.append(((self.texture[self.map[row][col]]), iso_x, iso_y))
                # We have to be able to move the camera so despite the performance hit, it would be nessecary to utilize a camera.
    

      


