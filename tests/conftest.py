"""Configurações globais e fixtures para a suíte de testes com pytest."""

import pytest

from src.domain.entities.cliente import Cliente
from src.domain.entities.endereco import Endereco
from src.domain.entities.produto import Produto


@pytest.fixture
def app_client():
    """Fixture de cliente de aplicação (reservada para futuras integrações)."""
    return None


@pytest.fixture
def produto_exemplo():
    """Fixture utilitária fornecendo um produto válido padrão."""
    return Produto(nome="Produto Exemplo", preco=25.0)


@pytest.fixture
def endereco_exemplo():
    """Fixture utilitária fornecendo um endereço válido padrão."""
    return Endereco(rua="Rua das Acácias", numero="42")


@pytest.fixture
def cliente_exemplo(endereco_exemplo):
    """Fixture utilitária fornecendo um cliente válido padrão com endereço associado."""
    return Cliente(
        nome="Cliente Padrão",
        telefone="11988887777",
        endereco=endereco_exemplo,
    )
