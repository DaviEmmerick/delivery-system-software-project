"""Testes unitários para a entidade Entrega."""

import pytest

from src.domain.entities.entrega import Entrega


def test_entrega_criacao_com_status_padrao():
    """Valida que o status inicial padrão de uma entrega é 'pendente'."""
    entrega = Entrega(pedido_id="PED-001")
    assert entrega.pedido_id == "PED-001"
    assert entrega.status == "pendente"


def test_entrega_criacao_com_status_customizado():
    """Valida instanciação informando um status de entrega personalizado."""
    entrega = Entrega(pedido_id="PED-002", status="em_transito")
    assert entrega.pedido_id == "PED-002"
    assert entrega.status == "em_transito"


def test_entrega_status_entregue():
    """Valida criação de entrega com status 'entregue'."""
    entrega = Entrega(pedido_id="PED-003", status="entregue")
    assert entrega.status == "entregue"


def test_entrega_deve_remover_espacos_em_branco_do_pedido_id():
    """Garante remoção de espaços em branco ao redor de pedido_id."""
    entrega = Entrega(pedido_id="  PED-003  ")
    assert entrega.pedido_id == "PED-003"


@pytest.mark.parametrize("pedido_id_invalido", [None, "", "   "])
def test_entrega_pedido_id_invalido_deve_lancar_excecao(pedido_id_invalido):
    """Garante que pedido_id nulo, vazio ou somente espaços lance ValueError."""
    with pytest.raises(ValueError, match="pedido_id é obrigatório"):
        Entrega(pedido_id=pedido_id_invalido)
