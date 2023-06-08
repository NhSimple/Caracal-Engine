import pygame
import typing
import threading
import json
import os


def threaded(fn):
    def wrapper(*args, **kwargs):
        # daemon thread so that the thread is deleted when the main thread exits
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


class ChunkManager:
    def __init__(self) -> None:
        self.map: typing.Dict[typing.List[typing.List[int]]] = None
        self.worldFolderDir: str = "worlds"
        self.mapName: str = None
        self.generatedChunks: typing.List[typing.Tuple[int, int]] = None

    def generateChunk(self, chunkPos: typing.Tuple[int, int]):
        pass

    def parseMap(self, mapdata: dict):
        pass

    def loadMap(self, mapName: str):
        self.mapName = mapName
        path = os.path.join(os.getcwd(), self.worldFolderDir, mapName + ".json")
        with open(path, "r") as f:
            data = json.load(f)
        self.parseMap(data)

    def saveMap(self):
        pass

    def saveChunk(self, chunkPos: typing.Tuple[int, int]):
        pass

    def loadChunk(self, chunkPos: typing.Tuple[int, int]):
        pass

    def draw(self):
        pass


if __name__ == "__main__":
    mg = ChunkManager()
    mg.loadMap("test")
