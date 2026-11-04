from src.domain.entities.restaurante import Restaurante
from tests.fakes import FakeRepository


def test_fake_repository_adiciona_busca_e_lista_entidades():
    repository = FakeRepository[Restaurante]()
    restaurante = Restaurante("Restaurante Central")

    repository.add(restaurante)

    assert repository.get(restaurante.id) is restaurante
    assert repository.list() == [restaurante]


def test_fake_repository_retorna_none_para_id_desconhecido():
    repository = FakeRepository[Restaurante]()

    assert repository.get("inexistente") is None