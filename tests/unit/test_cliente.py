import pytest
from src.domain.entities.cliente import Cliente
from src.domain.entities.endereco import Endereco


def test_cliente_criacao_com_sucesso():
    cliente = Cliente(nome="João Silva", telefone="11999998888")
    assert cliente.nome == "João Silva"
    assert cliente.telefone == "11999998888"
    assert cliente.endereco is None
    assert cliente.id is not None
    assert isinstance(cliente.id, str)
    assert len(cliente.id) == 32


def test_cliente_criacao_com_id_customizado():
    cliente = Cliente(
        nome="João Silva",
        telefone="11999998888",
        id="cliente-custom-123",
    )
    assert cliente.id == "cliente-custom-123"


def test_cliente_criacao_com_endereco():
    endereco = Endereco(rua="Rua das Flores", numero="123")
    cliente = Cliente(
        nome="João Silva",
        telefone="11999998888",
        endereco=endereco,
    )
    assert cliente.endereco == endereco


@pytest.mark.parametrize("endereco_invalido", ["Rua A, 100", 123, {"rua": "A"}])
def test_cliente_endereco_invalido_deve_lancar_excecao(endereco_invalido):
    with pytest.raises(ValueError, match="endereco deve ser um Endereco"):
        Cliente(nome="João Silva", telefone="11999998888", endereco=endereco_invalido)


def test_cliente_deve_remover_espacos_em_branco():
    cliente = Cliente(nome="  Maria Souza  ", telefone="  11888887777  ")
    assert cliente.nome == "Maria Souza"
    assert cliente.telefone == "11888887777"


@pytest.mark.parametrize("nome_invalido", [None, "", "   "])
def test_cliente_nome_invalido_deve_lancar_excecao(nome_invalido):
    with pytest.raises(ValueError, match="nome é obrigatório"):
        Cliente(nome=nome_invalido, telefone="11999998888")


@pytest.mark.parametrize("telefone_invalido", [None, "", "   ", "123456789", "  12345  "])
def test_cliente_telefone_invalido_deve_lancar_excecao(telefone_invalido):
    with pytest.raises(ValueError, match="telefone inválido"):
        Cliente(nome="João Silva", telefone=telefone_invalido)


def test_cliente_telefone_com_tamanho_minimo_valido():
    cliente = Cliente(nome="João Silva", telefone="1133334444")
    assert cliente.telefone == "1133334444"
