from enum import IntEnum, auto


class ReturnCodes(IntEnum):
    NORMAL = None
    DELETED = auto()


class Entity:
    def __init__(self) -> None:
        pass

    # To be overridden by child classes
    def check_death(self):
        pass

    # To be overridden by child classes
    def update(self, dt):
        pass

    def _update(self, dt):
        self.update(dt)
        if self.check_death():
            return ReturnCodes.DELETED
        else:
            return ReturnCodes.NORMAL

    # To be overridden by child classes
    def draw(self):
        pass
