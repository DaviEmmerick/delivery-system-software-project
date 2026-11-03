from src.adapters.orm import create_sqlite_engine
from src.adapters.repository import RestauranteRepository
from src.domain.entities.produto import Produto
from src.domain.entities.restaurante import Restaurante


def test_restaurante_repository_preserva_produtos_no_round_trip():
    repository = RestauranteRepository(create_sqlite_engine())
    restaurante = Restaurante(
        nome="Pizzaria",
        produtos=[Produto("Pizza", 40.0), Produto("Suco", 8.5)],
    )

    repository.add(restaurante)
    recuperado = repository.get(restaurante.id)

    assert recuperado is not None
    assert recuperado.id == restaurante.id
    assert recuperado.nome == restaurante.nome
    assert [(produto.nome, produto.preco) for produto in recuperado.produtos] == [
        ("Pizza", 40.0),
        ("Suco", 8.5),
    ]