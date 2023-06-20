from dataclasses import dataclass


class Component:
    def __init__(self, object) -> None:
        self.object = object

    def _(self):
        from Caracal.Entities.entity import Entity
        self.object: Entity
    
    # to be overridden, called every frame
    def update(self, dt):
        pass
