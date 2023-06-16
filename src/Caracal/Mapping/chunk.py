import typing


class Chunk:
    def __init__(self, terrainData) -> None:
        self.terrainData: typing.List[typing.List[int]] = terrainData
        self.surf = None
