"""Testes unitários para o objeto de valor ItemPedido."""

from dataclasses import FrozenInstanceError

import pytest

from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.produto import Produto


def test_item_pedido_criacao_com_quantidade_padrao():
    """Valida instanciação de ItemPedido com quantidade padrão igual a 1."""
    produto = Produto(nome="Hambúrguer", preco=30.0)
    item = ItemPedido(produto=produto)

    assert item.produto == produto
    assert item.quantidade == 1
    assert item.subtotal == 30.0


def test_item_pedido_criacao_com_quantidade_customizada():
    """Valida instanciação com quantidade personalizada e cálculo correto de subtotal."""
    produto = Produto(nome="Refrigerante", preco=8.5)
    item = ItemPedido(produto=produto, quantidade=3)

    assert item.produto == produto
    assert item.quantidade == 3
    assert item.subtotal == pytest.approx(25.5)


@pytest.mark.parametrize("produto_invalido", [None, "produto_invalido", 123, {"nome": "pizza"}])
def test_item_pedido_produto_invalido_deve_lancar_excecao(produto_invalido):
    """Garante que produto que não seja instância de Produto lance ValueError."""
    with pytest.raises(ValueError, match="produto do item deve ser um Produto"):
        ItemPedido(produto=produto_invalido)


@pytest.mark.parametrize("quantidade_invalida", [0, -1, -5, True, False, 1.5, "2", None])
def test_item_pedido_quantidade_invalida_deve_lancar_excecao(quantidade_invalida):
    """Garante que quantidade não positiva ou de tipo não-inteiro lance ValueError."""
    produto = Produto(nome="Batata Frita", preco=12.0)
    with pytest.raises(ValueError, match="quantidade deve ser um inteiro positivo"):
        ItemPedido(produto=produto, quantidade=quantidade_invalida)


def test_item_pedido_imutabilidade():
    """Valida que atributos de ItemPedido não podem ser alterados após instanciação."""
    produto = Produto(nome="Pizza", preco=40.0)
    item = ItemPedido(produto=produto, quantidade=2)

    with pytest.raises(FrozenInstanceError):
        item.quantidade = 3

    with pytest.raises(FrozenInstanceError):
        item.produto = Produto(nome="Outra Pizza", preco=50.0)


def test_item_pedido_igualdade_por_valor():
    """Valida igualdade estrutural entre dois itens de pedido com mesmos dados."""
    produto = Produto(nome="Suco", preco=7.0)
    item1 = ItemPedido(produto=produto, quantidade=2)
    item2 = ItemPedido(produto=produto, quantidade=2)

    assert item1 == item2
