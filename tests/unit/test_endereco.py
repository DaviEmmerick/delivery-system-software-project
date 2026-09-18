import pytest
from src.domain.entities.endereco import Endereco


def test_endereco_criacao_com_sucesso():
    endereco = Endereco(rua="Av. Paulista", numero="1000")
    assert endereco.rua == "Av. Paulista"
    assert endereco.numero == "1000"


def test_endereco_deve_remover_espacos_em_branco():
    endereco = Endereco(rua="  Rua das Flores  ", numero="  123 A  ")
    assert endereco.rua == "Rua das Flores"
    assert endereco.numero == "123 A"


@pytest.mark.parametrize("rua_invalida", [None, "", "   "])
def test_endereco_rua_invalida_deve_lancar_excecao(rua_invalida):
    with pytest.raises(ValueError, match="rua é obrigatória"):
        Endereco(rua=rua_invalida, numero="100")


@pytest.mark.parametrize("numero_invalido", [None, "", "   "])
def test_endereco_numero_invalido_deve_lancar_excecao(numero_invalido):
    with pytest.raises(ValueError, match="número é obrigatório"):
        Endereco(rua="Rua das Flores", numero=numero_invalido)
