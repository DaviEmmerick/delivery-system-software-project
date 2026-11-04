from src.adapters.repository import AbstractRepository
from src.domain.entities.restaurante import Restaurante


class FakeRepository(AbstractRepository[Restaurante]):
    def __init__(self) -> None:
        self._entities: dict[str, Restaurante] = {}

    def add(self, entity: Restaurante) -> None:
        self._entities[entity.id] = entity

    def get(self, entity_id: str) -> Restaurante | None:
        return self._entities.get(entity_id)

    def list(self) -> list[Restaurante]:
        return list(self._entities.values())


def test_fake_repository_adiciona_busca_e_lista_entidades():
    repository = FakeRepository()
    restaurante = Restaurante("Restaurante Central")

    repository.add(restaurante)

    assert repository.get(restaurante.id) is restaurante
    assert repository.list() == [restaurante]


def test_fake_repository_retorna_none_para_id_desconhecido():
    repository = FakeRepository()

    assert repository.get("inexistente") is None