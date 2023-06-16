import typing

from src.Caracal.Entities.entity import ReturnCodes, Entity


class EntityManager:
    def __init__(self) -> None:
        self.entities: typing.List[
            Entity
        ] = []  # Type hint not entirely correct, objects will be subclasses of Entity

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def update(self, dt):
        for entity in self.entities:
            returncode = entity._update(dt)
            if returncode == ReturnCodes.DELETED:
                self.remove_entity(entity)

    def draw(self, surf):
        for entity in self.entities:
            entity.draw(surf)
