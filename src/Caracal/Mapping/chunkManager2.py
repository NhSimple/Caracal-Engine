import pygame
import typing
import threading
import json
import os

from Caracal.Mapping.chunkGenerator import ChunkGenerator
from Caracal.Mapping.chunk import Chunk


def threaded(fn):
    def wrapper(*args, **kwargs):
        # daemon thread so that the thread is deleted when the main thread exits
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


class ChunkManager:
    def __init__(self, app) -> None:
        self.app = app
        #                 {  (0, 0) : ChunkObject               }
        self.map: typing.Dict[typing.List[int, int], Chunk] = None
        self.worldFolderDir: str = "worlds"
        self.mapName: str = None
        self.generatedChunks: typing.List[typing.Tuple[int, int]] = None
        self.chunkGenerator = ChunkGenerator()

    def _(self):
        from Caracal.game import Game
        self.app: Game

    def createChunk(self, chunkPos: typing.Tuple[int, int]):
        chunk = self.chunkGenerator.generate_chunk(chunkPos)
        self.map[chunkPos] = chunk
        self.generatedChunks.append(chunkPos)

    def loadMap(self, mapName: str):
        self.mapName = mapName
        path = os.path.join(os.getcwd(), self.worldFolderDir, self.mapName, "info.json")
        with open(path, "r") as f:  # worlds/mapName/info.json
            data = json.load(f)
        self.parseMap(data)

    def parseMap(self, mapData: dict):
        self.chunkGenerator.seed = mapData["mapSeed"]
        self.chunkGenerator.generatedChunks.extend(mapData["generatedChunks"])
        self.app#.player.stuff = mapData["player"]

    def saveMap(self):
        path = os.path.join(os.getcwd(), self.worldFolderDir, self.mapName, "info.json")
        exportData = {}
        exportData["mapSeed"] = self.chunkGenerator.seed
        exportData["generatedChunks"] = self.chunkGenerator.generatedChunks
        # exportData["player"] = self.app.player.stuff
        with open(path, "w") as f:  # worlds/mapName/info.json
            json.dump(f, exportData)

    def saveChunk(self, chunk: Chunk, chunkPos: typing.Tuple[int, int]):
        path = os.path.join(os.getcwd(), self.worldFolderDir, self.mapName, "chunks",f"{chunkPos}.json")
        exportData = {}
        exportData["terrainData"] = chunk.terrainData
        with open(path, "w") as f:
            json.dump(f, exportData)

    def loadChunk(self, chunkPos: typing.Tuple[int, int]):
        """
            Assumes that the chunk has been generated before.
        """
        path = os.path.join(os.getcwd(), self.worldFolderDir, self.mapName, "chunks",f"{chunkPos}.json")
        with open(path, "r") as f:
            data = json.load(f)

        self.map["chunkpos"] = Chunk(data["terrainData"])

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
