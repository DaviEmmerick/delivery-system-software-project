from __future__ import annotations
import math
from typing import Protocol, TypeVar, runtime_checkable
from src.domain.model import Cliente, Endereco, Entrega, ItemPedido, Pedido, Produto, Restaurante

T = TypeVar("T")

STATUS_ENTREGA = ("pendente", "em_transito", "entregue", "cancelada")


@runtime_checkable
class LeitorRepositorio(Protocol[T]):
    """Protocolo segregado para leitura pontual por identificador (ISP)."""

    def get(self, entity_id: str) -> T | None:
        ...


@runtime_checkable
class ListadorRepositorio(Protocol[T]):
    """Protocolo segregado para listagem de coleções de entidades (ISP)."""

    def list(self) -> list[T]:
        ...


@runtime_checkable
class EscritorRepositorio(Protocol[T]):
    """Protocolo segregado para adição/persistência de entidades (ISP)."""

    def add(self, entity: T) -> None:
        ...


@runtime_checkable
class Repositorio(LeitorRepositorio[T], ListadorRepositorio[T], EscritorRepositorio[T], Protocol[T]):
    """Contrato abstrato completo de repositório composto pelas interfaces segregadas (ISP e DIP)."""
    ...


class EntregaMemoryRepository:
    """Implementação padrão em memória do contrato Repositorio[Entrega] indexada por pedido_id."""

    def __init__(self) -> None:
        self._dados: dict[str, Entrega] = {}

    def add(self, entity: Entrega) -> None:
        self._dados[entity.pedido_id] = entity

    def get(self, entity_id: str) -> Entrega | None:
        return self._dados.get(entity_id)

    def list(self) -> list[Entrega]:
        return list(self._dados.values())


class NaoEncontrado(ValueError):
    """Recurso pedido não existe (a API responde 404)."""


class Conflito(ValueError):
    """Operação viola uma unicidade, ex.: telefone já cadastrado (a API responde 409)."""


def criar_cliente(
    nome: str,
    telefone: str,
    rua: str | None,
    numero: str | None,
    cliente_repo: Repositorio[Cliente],
) -> str:
    endereco = None
    if rua is not None or numero is not None:
        endereco = Endereco(rua=rua, numero=numero)
    cliente = Cliente(nome=nome, telefone=telefone, endereco=endereco)
    if any(existente.telefone == cliente.telefone for existente in cliente_repo.list()):
        raise Conflito("telefone já cadastrado")
    cliente_repo.add(cliente)
    return cliente.id


def consultar_cliente(cliente_id: str, cliente_repo: LeitorRepositorio[Cliente]) -> Cliente:
    cliente = cliente_repo.get(cliente_id)
    if cliente is None:
        raise NaoEncontrado("cliente não encontrado")
    return cliente


def criar_restaurante(
    nome: str,
    restaurante_repo: Repositorio[Restaurante],
    produtos: list[dict] | None = None,
) -> str:
    if produtos is not None and not isinstance(produtos, list):
        raise ValueError("produtos devem ser uma lista")
    produtos_entidades = [_montar_produto(produto) for produto in (produtos or [])]
    restaurante = Restaurante(nome=nome, produtos=produtos_entidades)
    if any(existente.nome == restaurante.nome for existente in restaurante_repo.list()):
        raise Conflito("restaurante já cadastrado")
    restaurante_repo.add(restaurante)
    return restaurante.id


def listar_restaurantes(restaurante_repo: ListadorRepositorio[Restaurante]) -> list[Restaurante]:
    return restaurante_repo.list()


def _montar_produto(dado) -> Produto:
    if not isinstance(dado, dict):
        raise ValueError("cada produto deve ser um objeto com nome e preco")
    nome, preco = dado.get("nome"), dado.get("preco")
    if not isinstance(nome, str):
        raise ValueError("nome do produto é obrigatório")
    if isinstance(preco, bool) or not isinstance(preco, (int, float)) or not math.isfinite(preco):
        raise ValueError("preco do produto deve ser um número")
    return Produto(nome=nome, preco=preco)


def _montar_item(dado) -> ItemPedido:
    produto = _montar_produto(dado)
    return ItemPedido(produto, quantidade=dado.get("quantidade", 1))


def criar_pedido(
    cliente_id: str,
    produtos: list[dict],
    cliente_repo: LeitorRepositorio[Cliente],
    pedido_repo: EscritorRepositorio[Pedido],
    entregas: EscritorRepositorio[Entrega],
) -> str:
    consultar_cliente(cliente_id, cliente_repo)
    if not isinstance(produtos, list) or not produtos:
        raise ValueError("pedido deve conter ao menos um item")
    itens = [_montar_item(produto) for produto in produtos]
    pedido = Pedido(cliente=cliente_id, itens=itens)
    pedido_repo.add(pedido)
    entregas.add(Entrega(pedido_id=pedido.id))
    return pedido.id


def consultar_pedido(pedido_id: str, pedido_repo: LeitorRepositorio[Pedido]) -> Pedido:
    pedido = pedido_repo.get(pedido_id)
    if pedido is None:
        raise NaoEncontrado("pedido não encontrado")
    return pedido


def listar_pedidos_do_cliente(
    cliente_id: str,
    cliente_repo: LeitorRepositorio[Cliente],
    pedido_repo: ListadorRepositorio[Pedido],
) -> list[Pedido]:
    consultar_cliente(cliente_id, cliente_repo)
    return [pedido for pedido in pedido_repo.list() if pedido.cliente == cliente_id]


def consultar_status_entrega(
    pedido_id: str,
    entregas: LeitorRepositorio[Entrega],
) -> str:
    entrega = entregas.get(pedido_id)
    if entrega is None:
        raise NaoEncontrado("entrega não encontrada")
    return entrega.status


def atualizar_status_entrega(
    pedido_id: str,
    novo_status: str,
    entregas: Repositorio[Entrega],
) -> str:
    entrega = entregas.get(pedido_id)
    if entrega is None:
        raise NaoEncontrado("entrega não encontrada")
    if not isinstance(novo_status, str):
        raise ValueError(f"status inválido; use um de: {', '.join(STATUS_ENTREGA)}")
    status_normalizado = novo_status.strip()
    if status_normalizado not in STATUS_ENTREGA:
        raise ValueError(f"status inválido; use um de: {', '.join(STATUS_ENTREGA)}")
    entrega.atualizar_status(status_normalizado)
    entregas.add(entrega)
    return entrega.status
