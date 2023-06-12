import pygame
import typing
import threading
import json
import os

from src.Caracal.Mapping.chunkGenerator import ChunkGenerator
from src.Caracal.Mapping.chunk import Chunk


def threaded(fn):
    def wrapper(*args, **kwargs):
        # daemon thread so that the thread is deleted when the main thread exits
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


class ChunkManager:
    def __init__(self) -> None:
        #                 {  (0, 0) : ChunkObject               }
        self.map: typing.Dict[typing.List[int, int], Chunk] = None
        self.worldFolderDir: str = "worlds"
        self.mapName: str = None
        self.generatedChunks: typing.List[typing.Tuple[int, int]] = None
        self.chunkGenerator = ChunkGenerator()

    def createChunk(self, chunkPos: typing.Tuple[int, int]):
        chunk = self.chunkGenerator.generate_chunk(chunkPos)
        self.map[chunkPos] = chunk

    def loadMap(self, mapName: str):
        self.mapName = mapName
        path = os.path.join(os.getcwd(), self.worldFolderDir, mapName + ".json")
        with open(path, "r") as f:
            data = json.load(f)
        self.parseMap(data)

    def parseMap(self, mapdata: dict):
        pass

    def saveMap(self):
        pass

    def saveChunk(self, chunkPos: typing.Tuple[int, int]):
        pass

    def loadChunk(self, chunkPos: typing.Tuple[int, int]):
        pass

    def draw(self):
        pass

    def _calculateChunksToDraw(self, chunk: Chunk):
        rect: pygame.Rect = createRect(chunk.terrainData[0])  # get the first element
        for tile in chunk.terrainData:  # get the entire rect size of the chunk
            tileRect: pygame.Rect = createRect(tile)
            rect = rect.union(tileRect)

        if rect.collideRect(screenRect):  # visible, draw chunk
            pass
        else:  # not visible
            pass

        chunksToDraw = None
