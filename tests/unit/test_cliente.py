"""Testes unitários para a entidade Cliente."""

import pytest

from src.domain.entities.cliente import Cliente
from src.domain.entities.endereco import Endereco


def test_cliente_criacao_com_sucesso():
    """Valida criação de cliente com campos obrigatórios e id gerado automaticamente."""
    cliente = Cliente(nome="João Silva", telefone="11999998888")
    assert cliente.nome == "João Silva"
    assert cliente.telefone == "11999998888"
    assert cliente.endereco is None
    assert cliente.id is not None
    assert isinstance(cliente.id, str)
    assert len(cliente.id) == 32


def test_cliente_criacao_com_id_customizado():
    """Valida atribuição correta de id customizado fornecido na instanciação."""
    cliente = Cliente(
        nome="João Silva",
        telefone="11999998888",
        id="cliente-custom-123",
    )
    assert cliente.id == "cliente-custom-123"


def test_cliente_criacao_com_endereco():
    """Valida associação de um objeto de valor Endereco ao cliente."""
    endereco = Endereco(rua="Rua das Flores", numero="123")
    cliente = Cliente(
        nome="João Silva",
        telefone="11999998888",
        endereco=endereco,
    )
    assert cliente.endereco == endereco


@pytest.mark.parametrize("endereco_invalido", ["Rua A, 100", 123, {"rua": "A"}])
def test_cliente_endereco_invalido_deve_lancar_excecao(endereco_invalido):
    """Garante que fornecer endereço que não seja instância de Endereco lança ValueError."""
    with pytest.raises(ValueError, match="endereco deve ser um Endereco"):
        Cliente(nome="João Silva", telefone="11999998888", endereco=endereco_invalido)


def test_cliente_deve_remover_espacos_em_branco():
    """Garante que espaços sobressalentes em nome e telefone sejam removidos."""
    cliente = Cliente(nome="  Maria Souza  ", telefone="  11888887777  ")
    assert cliente.nome == "Maria Souza"
    assert cliente.telefone == "11888887777"


@pytest.mark.parametrize("nome_invalido", [None, "", "   "])
def test_cliente_nome_invalido_deve_lancar_excecao(nome_invalido):
    """Garante que nome vazio, em branco ou nulo lance ValueError."""
    with pytest.raises(ValueError, match="nome é obrigatório"):
        Cliente(nome=nome_invalido, telefone="11999998888")


@pytest.mark.parametrize("telefone_invalido", [None, "", "   ", "123456789", "  12345  "])
def test_cliente_telefone_invalido_deve_lancar_excecao(telefone_invalido):
    """Garante que telefone nulo, vazio ou com menos de 10 dígitos lance ValueError."""
    with pytest.raises(ValueError, match="telefone inválido"):
        Cliente(nome="João Silva", telefone=telefone_invalido)


def test_cliente_telefone_com_tamanho_minimo_valido():
    """Garante aceitação de telefone com comprimento mínimo permitido (10 dígitos)."""
    cliente = Cliente(nome="João Silva", telefone="1133334444")
    assert cliente.telefone == "1133334444"
