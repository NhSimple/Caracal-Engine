import typing

# True means that this attribute will be saved to the chunk file.
CHUNK_ATTRIBUTES = {"pos": True, "terrainData": True, "surface": False}


class Chunk:
    def __init__(self) -> None:
        self.terrainData: typing.List[typing.List[int]] = None
        self.surf = None
