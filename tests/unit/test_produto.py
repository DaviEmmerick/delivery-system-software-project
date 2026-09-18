import pytest
from src.domain.entities.produto import Produto


def test_produto_criacao_com_sucesso():
    produto = Produto(nome="Hambúrguer Artesanal", preco=29.90)
    assert produto.nome == "Hambúrguer Artesanal"
    assert produto.preco == 29.90


def test_produto_deve_remover_espacos_em_branco_do_nome():
    produto = Produto(nome="  Batata Frita  ", preco=15.0)
    assert produto.nome == "Batata Frita"
    assert produto.preco == 15.0


def test_produto_converte_preco_inteiro_para_float():
    produto = Produto(nome="Refrigerante", preco=8)
    assert isinstance(produto.preco, float)
    assert produto.preco == 8.0


def test_produto_preco_zero_permitido():
    produto = Produto(nome="Molho Especial", preco=0)
    assert produto.preco == 0.0


@pytest.mark.parametrize("nome_invalido", [None, "", "   "])
def test_produto_nome_invalido_deve_lancar_excecao(nome_invalido):
    with pytest.raises(ValueError, match="nome do produto é obrigatório"):
        Produto(nome=nome_invalido, preco=25.0)


@pytest.mark.parametrize("preco_negativo", [-0.01, -1.0, -99.9])
def test_produto_preco_negativo_deve_lancar_excecao(preco_negativo):
    with pytest.raises(ValueError, match="preço não pode ser negativo"):
        Produto(nome="Pizza", preco=preco_negativo)
