import pytest

from src.adapters.orm import create_sqlite_engine
from src.adapters.repository import ClienteRepository, PedidoRepository, RestauranteRepository
from src.domain.entities.cliente import Cliente
from src.domain.entities.endereco import Endereco
from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.pedido_factory import PedidoFactory
from src.domain.entities.produto import Produto
from src.domain.entities.restaurante import Restaurante


@pytest.fixture
def repositories(tmp_path):
    database_path = (tmp_path / "delivery.sqlite3").as_posix()
    engine = create_sqlite_engine(f"sqlite+pysqlite:///{database_path}")
    yield (
        ClienteRepository(engine),
        PedidoRepository(engine),
        RestauranteRepository(engine),
    )
    engine.dispose()


def test_cliente_repository_persiste_endereco_e_identidade(repositories):
    cliente_repository, _, _ = repositories
    cliente = Cliente("Ana Souza", "11999998888", Endereco("Rua A", "10"))

    cliente_repository.add(cliente)
    recuperado = cliente_repository.get(cliente.id)

    assert recuperado is not None
    assert recuperado.id == cliente.id
    assert recuperado.nome == "Ana Souza"
    assert recuperado.endereco == Endereco("Rua A", "10")
    assert [item.id for item in cliente_repository.list()] == [cliente.id]


def test_pedido_repository_persiste_itens_quantidades_e_total(repositories):
    _, pedido_repository, _ = repositories
    pedido = PedidoFactory.criar(
        "Ana Souza",
        [
            ItemPedido(Produto("Pizza", 45.50), quantidade=2),
            Produto("Suco", 8.0),
        ],
    )

    pedido_repository.add(pedido)
    recuperado = pedido_repository.get(pedido.id)

    assert recuperado is not None
    assert recuperado.id == pedido.id
    assert [item.quantidade for item in recuperado.itens] == [2, 1]
    assert recuperado.total == pytest.approx(99.0)


def test_restaurante_repository_persiste_e_lista_restaurantes(repositories):
    _, _, restaurante_repository = repositories
    restaurante = Restaurante("Restaurante Central")

    restaurante_repository.add(restaurante)
    recuperado = restaurante_repository.get(restaurante.id)

    assert recuperado is not None
    assert recuperado.id == restaurante.id
    assert recuperado.nome == "Restaurante Central"
    assert [item.id for item in restaurante_repository.list()] == [restaurante.id]


def test_restaurante_repository_preserva_produtos_no_round_trip(repositories):
    _, _, repository = repositories
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
