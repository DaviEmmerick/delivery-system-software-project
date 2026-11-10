from typing import Generic, TypeVar

from src.adapters.repository import AbstractRepository


T = TypeVar("T")


class FakeRepository(AbstractRepository[T], Generic[T]):
    def __init__(self):
        self._entities: dict[str, T] = {}

    def add(self, entity: T) -> None:
        self._entities[entity.id] = entity

    def get(self, entity_id: str) -> T | None:
        return self._entities.get(entity_id)

    def list(self) -> list[T]:
        return list(self._entities.values())