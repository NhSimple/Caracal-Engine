from pygame import Surface

from Caracal.Entities.returnCodes import ReturnCodes
from Caracal.Entities.components.pos import Position
from Caracal.Entities.components.size import Size
from Caracal.Entities.components.sprite import SpriteRenderer


class Entity:
    def __init__(self, x: int = 0, y: int = 0, w: int | None = 0, h: int | None = 0, sprite: Surface = None) -> None:
        self.pos = Position(self, x=x, y=y)
        if sprite is None:
            sprite = Surface((1,1))
        if h is None:
            h = sprite.get_height()
        if w is None:
            w = sprite.get_width()
        self.size = Size(w=w, h=h)
        self.spriteRenderer = SpriteRenderer(self, sprite=sprite)

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
