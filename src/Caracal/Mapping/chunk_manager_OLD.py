from pygame import surface, draw
from typing import Dict
from os import listdir, remove
import json
import random
import time
import threading
from Caracal.Mapping.chunk import CHUNK_ATTRIBUTES
from Caracal.Mapping.chunkGenerator import ChunkGenerator


def threaded(fn):
    def wrapper(*args, **kwargs):
        # we make it a daemon thread so that the thread is
        # deleted when the main thread exits
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


class ChunkManager:
    def __init__(self, app, tile_sprs, CHUNK_SIZE, CHUNK_RADIUS, TILE_PIXEL_SIZE):
        self.app = app
        self.tile_sprs = tile_sprs
        self.centerpos = 0
        self.loaded_chunks: Dict[str, dict] = {}
        self.generated_chunks = []
        self.CHUNK_RADIUS = CHUNK_RADIUS
        self.CHUNK_WIDTH = CHUNK_SIZE[0]
        self.CHUNK_HEIGHT = CHUNK_SIZE[1]
        self.TILE_PIXEL_SIZE = TILE_PIXEL_SIZE
        self.testmode = False
        self.thread = None
        self.inmap = False
        self.world_root_dir = None
        self.chunk_generator = None

    def load_map(self, root_dir: str):
        self.world_root_dir = root_dir.rstrip("/")
        with open(self.world_root_dir + "/info.json", "r") as f:
            map_data = json.load(f)

        self.centerpos = map_data["player"]["chunkpos"]
        self.app.player.pos = map_data["player"]["playerpos"]
        self.generated_chunks = map_data["generated_chunks"]
        self.seed = map_data["map_seed"]
        self.chunk_generator = ChunkGenerator(self.seed)
        # opensimplex.seed(self.seed) TODO: worldgen & library
        self.inmap = True
        self.thread = self.manage_chunks()

    def new_map(self, root_dir: str, seed: int = None):
        self.delete_all_chunks()
        self.app.player.pos = [0, 0]
        self.centerpos = 0
        self.generated_chunks = []
        self.seed = random.randint(111_111_111, 999_999_999) if seed is None else seed
        self.chunk_generator = ChunkGenerator(self.seed)
        self.world_root_dir = root_dir.rstrip("/")
        # opensimplex.seed(self.seed)  TODO: worldgen & library
        print(f"GENERATED NEW MAP WITH SEED: {self.seed}")

        self.inmap = True
        self.thread = self.manage_chunks()

    def load_chunk(self, chunkpos):
        with open(
            self.world_root_dir + "/chunks/" + f"{chunkpos}.chunk", "r"
        ) as chunkfile:
            chunkdata = json.load(chunkfile)
            new_chunk = {}
            for key, value in CHUNK_ATTRIBUTES.items():
                if value:
                    new_chunk[key] = chunkdata[key]
                else:  # value will be generated, idk how to do that though
                    pass
            self.loaded_chunks[chunkpos] = new_chunk
            print(f"LOADED CHUNK {chunkpos}")
            self.generated_chunks.append(chunkpos)

    def draw(self, surf):
        for x in range(
            self.centerpos - (self.CHUNK_WIDTH // 2),
            self.centerpos + (self.CHUNK_WIDTH // 2),
        ):
            try:
                surf.blit(
                    self.loaded_chunks[x]["image"],
                    (
                        x * self.CHUNK_WIDTH * self.BLOCK_PIXEL_SIZE
                        - self.camera.pos[0],
                        -self.camera.pos[1],
                    ),
                )
            except KeyError:  # hasnt been generated yet
                xpos = x * self.CHUNK_WIDTH * self.BLOCK_PIXEL_SIZE - self.camera.pos[0]
                ypos = -self.camera.pos[1]
                draw.rect(
                    surf,
                    "black",
                    (
                        xpos,
                        ypos,
                        self.CHUNK_WIDTH * self.BLOCK_PIXEL_SIZE,
                        self.CHUNK_HEIGHT * self.BLOCK_PIXEL_SIZE,
                    ),
                )

    def set_centerpos(self, new_x: int):
        self.calc_centerpos(new_x)

    def calc_centerpos(self, new_x):
        self.centerpos = new_x // (
            self.CHUNK_WIDTH * self.BLOCK_PIXEL_SIZE
        )  # update pos

    @threaded
    def manage_chunks(self):
        while self.inmap:
            center_chunkx = self.centerpos
            for x in range(
                center_chunkx - self.chunkradius, center_chunkx + self.chunkradius
            ):
                if self.loaded_chunks.get(x):  # Chunk Found
                    pass
                else:  # chunk not found
                    # if we generated it already
                    if x in self.generated_chunks:
                        self.load_chunk(x)
                    else:  # we havent generated the chunk before
                        self.generate_new_chunk(x)
                        # I dont need to call threading.Thread since
                        # the function uses @threaded wrapper

            chunkstounload = []
            for chunk in self.loaded_chunks:
                # if chunk is far away
                if abs(chunk - center_chunkx) > self.chunkradius:
                    chunkstounload.append(chunk)

            for c in chunkstounload:
                self.unload_chunk(c)

            time.sleep(1 / 60)
        print("CHUNK_GENERATOR THREAD WILL NOW EXIT")

    def unload_all_chunks(self):
        self.inmap = False
        self.thread.join()
        self.chunk_generator = None
        chunks = list(self.loaded_chunks.keys()).copy()
        for c in chunks:
            self.unload_chunk(c)
        print("UNLOADED EVERYTHING")

        with open(self.world_root_dir + "/info.json", "w") as file:
            data = {}
            data["player"] = {
                "chunkpos": self.centerpos,
                "playerpos": self.app.player.pos,
                "inventory": [],
            }
            data["generated_chunks"] = self.generated_chunks
            data["map_seed"] = self.seed
            json.dump(data, file)

    def unload_chunk(self, chunkpos):
        with open(
            self.world_root_dir + "/chunks/" + f"{chunkpos}.chunk", "w"
        ) as chunkfile:
            self.loaded_chunks[chunkpos].pop("image")
            json.dump(self.loaded_chunks[chunkpos], chunkfile)

        self.loaded_chunks.pop(chunkpos)
        print(f"UNLOADED CHUNK: {chunkpos}")

    def generate_new_chunk(self, chunkpos):
        start_time = time.time()
        print(f"Started generating chunk {chunkpos} with thread")
        tiledata = self.generate_chunk_terrain(chunkpos)
        lightdata = self.generate_lightdata(tiledata, chunkpos)
        self.loaded_chunks[chunkpos] = {
            "tiledata": tiledata,  # maybe np array?
            "entitydata": [],  # array([])}
            "lightdata": lightdata,
            "image": self.render_chunk(tiledata, lightdata),
        }
        self.generated_chunks.append(chunkpos)

    def reset_map(self):
        self.inmap = False
        self.thread.join()

        self.loaded_chunks = {}
        self.generated_chunks = []
        self.delete_all_chunks()

        self.inmap = True
        self.thread = self.manage_chunks()

    def delete_all_chunks(self):
        path = self.world_root_dir + "/chunks/"
        chunkfiles = listdir(path)
        for f in chunkfiles:
            if f.endswith(".chunk"):
                remove(path + f)
        print("DELETED EVERY CHUNK")

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def clamp_chunk_width(self, val):
        return max(0, min(val, self.CHUNK_WIDTH - 1))

    def clamp_chunk_height(self, val):
        return max(0, min(val, self.CHUNK_HEIGHT - 1))
