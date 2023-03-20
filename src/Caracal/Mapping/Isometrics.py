


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


    def calculate(self):
        #method created to reduce the load on the initialization method.
        pygame = self.pygame
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                # Calculate the position of the tile in isometric coordinates
                iso_x = (col - row) * self.tile_half_width
                iso_y = (col + row) * self.tile_half_height/4
                # Save the position of the tile as a tuple
                self.tiles.append((pygame.transform.rotate(pygame.transform.scale(pygame.image.load(self.texture[self.map[row][col]]),(self.tile_width,self.tile_height)), 0), self.camera_x+iso_x, self.camera_y+iso_y+20))
                
    

      


