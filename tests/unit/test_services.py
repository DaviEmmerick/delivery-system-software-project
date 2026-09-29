import pytest
from src.adapters.repository import AbstractRepository
from src.service_layer import services

class FakeRepository(AbstractRepository):

    def __init__(self):
        self._dados = {}
    def add(self, entity):
        self._dados[entity.id] = entity
    def get(self, entity_id):
        return self._dados.get(entity_id)
    def list(self):
        return list(self._dados.values())

@pytest.fixture
def cliente_repo():
    return FakeRepository()


@pytest.fixture
def restaurante_repo():
    return FakeRepository()


@pytest.fixture
def pedido_repo():
    return FakeRepository()


@pytest.fixture
def entregas():
    return {}


def _cliente(cliente_repo, nome="Ana", telefone="21999999999"):
    return services.criar_cliente(nome, telefone, None, None, cliente_repo)


def _pedido(cliente_id, cliente_repo, pedido_repo, entregas, produtos=None):
    produtos = produtos or [{"nome": "Pizza", "preco": 40.0}]
    return services.criar_pedido(cliente_id, produtos, cliente_repo, pedido_repo, entregas)


def test_criar_cliente_persiste_e_retorna_id(cliente_repo):
    cliente_id = services.criar_cliente("Ana", "21999999999", "Rua A", "10", cliente_repo)
    cliente = cliente_repo.get(cliente_id)
    assert cliente.nome == "Ana"
    assert cliente.endereco.rua == "Rua A"

def test_criar_cliente_com_endereco_incompleto_levanta_erro(cliente_repo):
    with pytest.raises(ValueError, match="número é obrigatório"):
        services.criar_cliente("Ana", "21999999999", "Rua A", None, cliente_repo)
    assert cliente_repo.list() == []


def test_criar_cliente_com_telefone_duplicado_levanta_conflito(cliente_repo):
    _cliente(cliente_repo, "Ana", "21999999999")
    with pytest.raises(services.Conflito):
        _cliente(cliente_repo, "Outra Ana", " 21999999999 ")
    assert len(cliente_repo.list()) == 1


def test_consultar_cliente_inexistente_levanta_nao_encontrado(cliente_repo):
    with pytest.raises(services.NaoEncontrado):
        services.consultar_cliente("nao-existe", cliente_repo)


def test_criar_e_listar_restaurantes(restaurante_repo):
    services.criar_restaurante("Cantina", restaurante_repo)
    services.criar_restaurante("Pizzaria", restaurante_repo)
    nomes = [r.nome for r in services.listar_restaurantes(restaurante_repo)]
    assert sorted(nomes) == ["Cantina", "Pizzaria"]


def test_criar_restaurante_duplicado_levanta_conflito(restaurante_repo):
    services.criar_restaurante("Cantina", restaurante_repo)
    with pytest.raises(services.Conflito):
        services.criar_restaurante("  Cantina ", restaurante_repo)


def test_criar_pedido_calcula_total_com_quantidade(cliente_repo, pedido_repo, entregas):
    cliente_id = _cliente(cliente_repo)
    produtos = [{"nome": "Pizza", "preco": 40.0, "quantidade": 2}, {"nome": "Suco", "preco": 7.5}]
    pedido_id = _pedido(cliente_id, cliente_repo, pedido_repo, entregas, produtos)

    pedido = services.consultar_pedido(pedido_id, pedido_repo)
    assert pedido.cliente == cliente_id
    assert pedido.total == pytest.approx(87.5)

def test_criar_pedido_cria_entrega_pendente(cliente_repo, pedido_repo, entregas):
    cliente_id = _cliente(cliente_repo)
    pedido_id = _pedido(cliente_id, cliente_repo, pedido_repo, entregas)
    assert services.consultar_status_entrega(pedido_id, entregas) == "pendente"


def test_criar_pedido_para_cliente_inexistente_nao_persiste_nada(cliente_repo, pedido_repo, entregas):
    with pytest.raises(services.NaoEncontrado):
        services.criar_pedido("fantasma", [{"nome": "X", "preco": 1}], cliente_repo, pedido_repo, entregas)
    assert pedido_repo.list() == []
    assert entregas == {}


@pytest.mark.parametrize(
    "produtos",
    [
        None,
        [],
        "abc",
        ["abc"],
        [{"preco": 10}],
        [{"nome": "X"}],
        [{"nome": "X", "preco": "abc"}],
        [{"nome": "X", "preco": True}],
        [{"nome": "X", "preco": float("nan")}],
        [{"nome": "X", "preco": -1}],
        [{"nome": "X", "preco": 10, "quantidade": 0}],
        [{"nome": "X", "preco": 10, "quantidade": "2"}],],)
def test_criar_pedido_com_produtos_invalidos_levanta_value_error(produtos, cliente_repo, pedido_repo, entregas):
    cliente_id = _cliente(cliente_repo)
    with pytest.raises(ValueError):
        services.criar_pedido(cliente_id, produtos, cliente_repo, pedido_repo, entregas)
    assert pedido_repo.list() == []
    assert entregas == {}

def test_consultar_pedido_inexistente_levanta_nao_encontrado(pedido_repo):
    with pytest.raises(services.NaoEncontrado):
        services.consultar_pedido("nao-existe", pedido_repo)


def test_listar_pedidos_do_cliente_retorna_so_os_dele(cliente_repo, pedido_repo, entregas):
    ana = _cliente(cliente_repo, "Ana", "21999999999")
    ana_2 = _cliente(cliente_repo, "Ana", "21988888888")  
    pedido_ana = _pedido(ana, cliente_repo, pedido_repo, entregas)
    _pedido(ana_2, cliente_repo, pedido_repo, entregas)

    pedidos = services.listar_pedidos_do_cliente(ana, cliente_repo, pedido_repo)
    assert [p.id for p in pedidos] == [pedido_ana]


def test_listar_pedidos_de_cliente_inexistente_levanta_nao_encontrado(cliente_repo, pedido_repo):
    with pytest.raises(services.NaoEncontrado):
        services.listar_pedidos_do_cliente("nao-existe", cliente_repo, pedido_repo)


@pytest.mark.parametrize("status", services.STATUS_ENTREGA)
def test_atualizar_status_entrega_aceita_status_validos(status, cliente_repo, pedido_repo, entregas):
    cliente_id = _cliente(cliente_repo)
    pedido_id = _pedido(cliente_id, cliente_repo, pedido_repo, entregas)
    assert services.atualizar_status_entrega(pedido_id, status, entregas) == status
    assert services.consultar_status_entrega(pedido_id, entregas) == status


@pytest.mark.parametrize("status", ["banana", "", None, 123])
def test_atualizar_status_entrega_rejeita_status_invalido(status, cliente_repo, pedido_repo, entregas):
    cliente_id = _cliente(cliente_repo)
    pedido_id = _pedido(cliente_id, cliente_repo, pedido_repo, entregas)
    with pytest.raises(ValueError, match="status inválido"):
        services.atualizar_status_entrega(pedido_id, status, entregas)
    assert services.consultar_status_entrega(pedido_id, entregas) == "pendente"


def test_atualizar_status_de_entrega_inexistente_levanta_nao_encontrado(entregas):
    with pytest.raises(services.NaoEncontrado):
        services.atualizar_status_entrega("nao-existe", "entregue", entregas)
