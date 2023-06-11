import pygame
import typing
import threading
import json
import os

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
        #                    {   (0,0):ChunkObject               }
        self.map: typing.Dict[typing.List[int, int], Chunk] = None
        self.worldFolderDir: str = "worlds"
        self.mapName: str = None
        self.generatedChunks: typing.List[typing.Tuple[int, int]] = None

    def generateChunk(self, chunkPos: typing.Tuple[int, int]):
        pass

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
        rect = createRect(someChunk[0])
        for tile in someChunk:  # get the entire rect size of the chunk
            tileRect = createRect(tile)
            rect = rect.union(tileRect)

        if rect.collideRect(screenRect):  # visible, draw chunk
            pass
        else:  # not visible
            pass

        chunksToDraw = None
