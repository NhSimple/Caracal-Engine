import opensimplex


class ChunkGenerator:
    def __init__(self, rust_generator, seed, CHUNK_WIDTH, CHUNK_HEIGHT):
        self.rust_generator = rust_generator  # Rust terrain generator module
        self.seed = seed
        self.CHUNK_WIDTH = CHUNK_WIDTH
        self.CHUNK_HEIGHT = CHUNK_HEIGHT
        opensimplex.seed(seed)

    def generate_chunk(self, chunkpos, chunk_metadata):
        self.rust_generator.generate_chunk(chunkpos, chunk_metadata)

    def render_chunk(self, terraindata, lightdata):
        chunk_surf = surface.Surface(
            (CHUNK_WIDTH * BLOCK_PIXEL_SIZE, CHUNK_HEIGHT * BLOCK_PIXEL_SIZE)
        )
        chunk_surf.fill(SKY_COLOR)
        opacity_surf = surface.Surface((16, 16))
        opacity_surf.fill("black")

        x, y = 0, 0
        for line in terraindata:
            x = 0
            for tile in line:
                light_level = lightdata[y][x]
                opacity_surf.set_alpha(light_level * 17)
                tile_surf = self.tile_sprs[tile].copy()
                tile_surf.blit(opacity_surf, (0, 0))

                chunk_surf.blit(tile_surf, (x * BLOCK_PIXEL_SIZE, y * BLOCK_PIXEL_SIZE))
                x += 1
            y += 1
        draw.line(
            chunk_surf, (0, 25, 255), (0, 0), (0, CHUNK_HEIGHT * BLOCK_PIXEL_SIZE), 2
        )

        return chunk_surf
