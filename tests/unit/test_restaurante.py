import pytest
from src.domain.entities.restaurante import Restaurante


def test_restaurante_criacao_com_sucesso():
    restaurante = Restaurante(nome="Pizzaria da Nonna")
    assert restaurante.nome == "Pizzaria da Nonna"


def test_restaurante_deve_remover_espacos_em_branco_do_nome():
    restaurante = Restaurante(nome="  Hamburgueria Central  ")
    assert restaurante.nome == "Hamburgueria Central"


@pytest.mark.parametrize("nome_invalido", [None, "", "   "])
def test_restaurante_nome_invalido_deve_lancar_excecao(nome_invalido):
    with pytest.raises(ValueError, match="nome é obrigatório"):
        Restaurante(nome=nome_invalido)
