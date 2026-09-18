import pytest
from src.domain.entities.pedido import Pedido
from src.domain.entities.produto import Produto


def test_pedido_criacao_com_sucesso_e_calculo_total():
    item1 = Produto(nome="Pizza", preco=45.50)
    item2 = Produto(nome="Refrigerante", preco=8.50)
    itens = [item1, item2]

    pedido = Pedido(cliente="Carlos Eduardo", itens=itens)

    assert pedido.cliente == "Carlos Eduardo"
    assert pedido.itens == itens
    assert pytest.approx(pedido.total) == 54.00


def test_pedido_deve_remover_espacos_em_branco_do_cliente():
    itens = [Produto(nome="Sanduíche", preco=20.0)]
    pedido = Pedido(cliente="  Carlos Eduardo  ", itens=itens)

    assert pedido.cliente == "Carlos Eduardo"


def test_pedido_com_um_unico_item():
    itens = [Produto(nome="Prato Feito", preco=25.0)]
    pedido = Pedido(cliente="Ana", itens=itens)

    assert pedido.total == 25.0


@pytest.mark.parametrize("cliente_invalido", [None, "", "   "])
def test_pedido_cliente_invalido_deve_lancar_excecao(cliente_invalido):
    itens = [Produto(nome="Suco", preco=7.0)]
    with pytest.raises(ValueError, match="cliente é obrigatório"):
        Pedido(cliente=cliente_invalido, itens=itens)


@pytest.mark.parametrize("itens_invalidos", [[], None])
def test_pedido_sem_itens_deve_lancar_excecao(itens_invalidos):
    with pytest.raises(ValueError, match="pedido deve conter ao menos um item"):
        Pedido(cliente="Ana", itens=itens_invalidos)
