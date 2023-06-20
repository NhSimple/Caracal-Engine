from pygame import Surface, display, transform

from Caracal.Entities.components.component import Component


class SpriteRenderer(Component):
    def __init__(self, object, sprite: Surface) -> None:
        super().__init__(object=object)
        self.sprite = sprite
    
    def flip(self, horizontal: bool = False, vertical: bool = False):
        self.sprite = transform.flip(self.sprite, flip_x=horizontal, flip_y=vertical)

    def draw(self, screen: Surface):
        screen.blit(self.sprite, )

    def _(self):
        from Caracal.Entities.entity import Entity
        self.object: Entity
