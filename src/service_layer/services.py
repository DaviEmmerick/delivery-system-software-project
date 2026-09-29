from __future__ import annotations
import math
from typing import TYPE_CHECKING
from src.domain.model import Cliente, Endereco, Entrega, ItemPedido, Pedido, Produto, Restaurante

if TYPE_CHECKING: 
    from src.adapters.repository import AbstractRepository
STATUS_ENTREGA = ("pendente", "em_transito", "entregue", "cancelada")

class NaoEncontrado(ValueError):
    """Recurso pedido não existe (a API responde 404)."""

class Conflito(ValueError):
    """Operação viola uma unicidade, ex.: telefone já cadastrado (a API responde 409)."""

def criar_cliente(
    nome: str,
    telefone: str,
    rua: str | None,
    numero: str | None,
    cliente_repo: AbstractRepository,
) -> str:
    endereco = None
    if rua is not None or numero is not None:
        endereco = Endereco(rua=rua, numero=numero) 
    cliente = Cliente(nome=nome, telefone=telefone, endereco=endereco)
    if any(existente.telefone == cliente.telefone for existente in cliente_repo.list()):
        raise Conflito("telefone já cadastrado")
    cliente_repo.add(cliente)
    return cliente.id

def consultar_cliente(cliente_id: str, cliente_repo: AbstractRepository) -> Cliente:
    cliente = cliente_repo.get(cliente_id)
    if cliente is None:
        raise NaoEncontrado("cliente não encontrado")
    return cliente

def criar_restaurante(nome: str, restaurante_repo: AbstractRepository) -> str:
    restaurante = Restaurante(nome=nome)
    if any(existente.nome == restaurante.nome for existente in restaurante_repo.list()):
        raise Conflito("restaurante já cadastrado")
    restaurante_repo.add(restaurante)
    return restaurante.id

def listar_restaurantes(restaurante_repo: AbstractRepository) -> list[Restaurante]:
    return restaurante_repo.list()

def _montar_item(dado) -> ItemPedido:
    if not isinstance(dado, dict):
        raise ValueError("cada produto deve ser um objeto com nome e preco")
    nome, preco = dado.get("nome"), dado.get("preco")
    if not isinstance(nome, str):
        raise ValueError("nome do produto é obrigatório")
    if isinstance(preco, bool) or not isinstance(preco, (int, float)) or not math.isfinite(preco):
        raise ValueError("preco do produto deve ser um número")
    return ItemPedido(Produto(nome=nome, preco=preco), quantidade=dado.get("quantidade", 1))

def criar_pedido(
    cliente_id: str,
    produtos: list[dict],
    cliente_repo: AbstractRepository,
    pedido_repo: AbstractRepository,
    entregas: dict[str, Entrega],
) -> str:
    consultar_cliente(cliente_id, cliente_repo)  
    if not isinstance(produtos, list) or not produtos:
        raise ValueError("pedido deve conter ao menos um item")
    itens = [_montar_item(produto) for produto in produtos]
    pedido = Pedido(cliente=cliente_id, itens=itens)  
    pedido_repo.add(pedido)
    entregas[pedido.id] = Entrega(pedido_id=pedido.id)
    return pedido.id

def consultar_pedido(pedido_id: str, pedido_repo: AbstractRepository) -> Pedido:
    pedido = pedido_repo.get(pedido_id)
    if pedido is None:
        raise NaoEncontrado("pedido não encontrado")
    return pedido

def listar_pedidos_do_cliente(
    cliente_id: str,
    cliente_repo: AbstractRepository,
    pedido_repo: AbstractRepository,
) -> list[Pedido]:
    consultar_cliente(cliente_id, cliente_repo)
    return [pedido for pedido in pedido_repo.list() if pedido.cliente == cliente_id]

def consultar_status_entrega(pedido_id: str, entregas: dict[str, Entrega]) -> str:
    entrega = entregas.get(pedido_id)
    if entrega is None:
        raise NaoEncontrado("entrega não encontrada")
    return entrega.status

def atualizar_status_entrega(pedido_id: str, novo_status: str, entregas: dict[str, Entrega]) -> str:
    entrega = entregas.get(pedido_id)
    if entrega is None:
        raise NaoEncontrado("entrega não encontrada")
    if novo_status not in STATUS_ENTREGA:
        raise ValueError(f"status inválido; use um de: {', '.join(STATUS_ENTREGA)}")
    entrega.status = novo_status
    return entrega.status
