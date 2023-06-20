from Caracal.Entities.components.component import Component


class Size(Component):
    def __init__(self, object, w: int = 0, h: int = 0) -> None:
        super().__init__(object=object)
        self.x = w
        self.y = h

    def _(self):
        from Caracal.Entities.entity import Entity
        self.object: Entity
