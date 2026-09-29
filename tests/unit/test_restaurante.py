"""Testes unitários para o agregado Restaurante."""

import pytest

from src.domain.entities.restaurante import Restaurante


def test_restaurante_criacao_com_sucesso():
    """Valida criação de restaurante com nome válido e id gerado automaticamente."""
    restaurante = Restaurante(nome="Pizzaria da Nonna")
    assert restaurante.nome == "Pizzaria da Nonna"
    assert restaurante.id is not None
    assert isinstance(restaurante.id, str)
    assert len(restaurante.id) == 32


def test_restaurante_criacao_com_id_customizado():
    """Valida que o id customizado informado no construtor é preservado."""
    restaurante = Restaurante(nome="Pizzaria da Nonna", id="rest-custom-123")
    assert restaurante.id == "rest-custom-123"


def test_restaurante_deve_remover_espacos_em_branco_do_nome():
    """Garante sanitização de espaços em branco ao redor do nome do restaurante."""
    restaurante = Restaurante(nome="  Hamburgueria Central  ")
    assert restaurante.nome == "Hamburgueria Central"


@pytest.mark.parametrize("nome_invalido", [None, "", "   "])
def test_restaurante_nome_invalido_deve_lancar_excecao(nome_invalido):
    """Garante que nome nulo ou vazio lance ValueError."""
    with pytest.raises(ValueError, match="nome é obrigatório"):
        Restaurante(nome=nome_invalido)
