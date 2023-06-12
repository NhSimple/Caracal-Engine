import opensimplex


class ChunkGenerator:
    def __init__(self, terrainGenerator, seed, CONST):
        self.terrainGenerator = terrainGenerator  # Rust terrain generator module
        self.seed = seed
        self.CONST = CONST
        opensimplex.seed(seed)

    def generate_chunk(self, chunkPos):
        data = self.terrainGenerator.generate_chunk(chunkPos)
        return data

    def render_chunk(self, terrainData, lightData):
        chunkSurf = surface.Surface(
            (self.CONST.CHUNK_WIDTH * BLOCK_PIXEL_SIZE, CHUNK_HEIGHT * BLOCK_PIXEL_SIZE)
        )
        chunkSurf.fill(SKY_COLOR)

        x, y = 0, 0
        for line in terrainData:
            x = 0
            for tile in line:
                tileSurf = self.tile_sprs[tile]
                chunkSurf.blit(tileSurf, (x * BLOCK_PIXEL_SIZE, y * BLOCK_PIXEL_SIZE))
                x += 1
            y += 1
        draw.line(
            chunkSurf, (0, 25, 255), (0, 0), (0, CHUNK_HEIGHT * BLOCK_PIXEL_SIZE), 2
        )

        return chunkSurf
