from Caracal.Entities.components.component import Component


class Position(Component):
    def __init__(self, object, x: int = 0, y: int = 0) -> None:
        super().__init__(object=object)
        self.x = x
        self.y = y
    
    def _(self):
        from Caracal.Entities.entity import Entity
        self.object: Entity
