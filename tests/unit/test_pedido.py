import pytest

from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.pedido import Pedido
from src.domain.entities.produto import Produto


def test_pedido_criacao_com_sucesso_a_partir_de_produtos():
    item1 = Produto(nome="Pizza", preco=45.50)
    item2 = Produto(nome="Refrigerante", preco=8.50)
    itens = [item1, item2]

    pedido = Pedido(cliente="Carlos Eduardo", itens=itens)

    assert pedido.cliente == "Carlos Eduardo"
    assert pedido.itens == (ItemPedido(item1), ItemPedido(item2))
    assert isinstance(pedido.itens, tuple)
    assert pytest.approx(pedido.total) == 54.00
    assert pedido.id is not None
    assert len(pedido.id) == 32


def test_pedido_criacao_com_id_customizado():
    item = Produto(nome="Sanduíche", preco=20.0)
    pedido = Pedido(cliente="Carlos", itens=[item], id="pedido-custom-999")
    assert pedido.id == "pedido-custom-999"


def test_pedido_criacao_com_itens_item_pedido():
    p1 = Produto(nome="Pizza", preco=40.0)
    p2 = Produto(nome="Refrigerante", preco=8.0)
    item1 = ItemPedido(produto=p1, quantidade=2)
    item2 = ItemPedido(produto=p2, quantidade=3)

    pedido = Pedido(cliente="Ana", itens=[item1, item2])

    assert pedido.itens == (item1, item2)
    assert pytest.approx(pedido.total) == (40.0 * 2) + (8.0 * 3)


def test_pedido_criacao_com_itens_mistos():
    p1 = Produto(nome="Hambúrguer", preco=25.0)
    p2 = Produto(nome="Batata Frita", preco=15.0)
    item2 = ItemPedido(produto=p2, quantidade=2)

    pedido = Pedido(cliente="Lucas", itens=[p1, item2])

    assert pedido.itens == (ItemPedido(p1), item2)
    assert pytest.approx(pedido.total) == 25.0 + 30.0


def test_pedido_deve_remover_espacos_em_branco_do_cliente():
    itens = [Produto(nome="Sanduíche", preco=20.0)]
    pedido = Pedido(cliente="  Carlos Eduardo  ", itens=itens)

    assert pedido.cliente == "Carlos Eduardo"


def test_pedido_com_um_unico_item():
    itens = [Produto(nome="Prato Feito", preco=25.0)]
    pedido = Pedido(cliente="Ana", itens=itens)

    assert pytest.approx(pedido.total) == 25.0


@pytest.mark.parametrize("cliente_invalido", [None, "", "   "])
def test_pedido_cliente_invalido_deve_lancar_excecao(cliente_invalido):
    itens = [Produto(nome="Suco", preco=7.0)]
    with pytest.raises(ValueError, match="cliente é obrigatório"):
        Pedido(cliente=cliente_invalido, itens=itens)


@pytest.mark.parametrize("itens_invalidos", [[], (), None])
def test_pedido_sem_itens_deve_lancar_excecao(itens_invalidos):
    with pytest.raises(ValueError, match="pedido deve conter ao menos um item"):
        Pedido(cliente="Ana", itens=itens_invalidos)


@pytest.mark.parametrize("item_invalido", ["string", 123, {"nome": "pizza"}])
def test_pedido_item_tipo_invalido_deve_lancar_excecao(item_invalido):
    with pytest.raises(ValueError, match="itens do pedido devem ser Produtos ou ItemPedido"):
        Pedido(cliente="Ana", itens=[item_invalido])
