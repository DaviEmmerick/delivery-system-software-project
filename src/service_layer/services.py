# Serviços do sistema de delivery.
from src.adapters.orm import create_sqlite_engine
from src.adapters.repository import ClienteRepository, PedidoRepository, RestauranteRepository
from src.domain.entities.cliente import Cliente
from src.domain.entities.endereco import Endereco
from src.domain.entities.entrega import Entrega
from src.domain.entities.pedido import Pedido
from src.domain.entities.produto import Produto
from src.domain.entities.restaurante import Restaurante

_engine = create_sqlite_engine()
_cliente_repo = ClienteRepository(_engine)
_restaurante_repo = RestauranteRepository(_engine)
_pedido_repo = PedidoRepository(_engine)

_entregas: dict[str, Entrega] = {}


def criar_cliente(nome: str, telefone: str, rua: str | None = None, numero: str | None = None) -> str:
    endereco = Endereco(rua=rua, numero=numero) if rua and numero else None
    cliente = Cliente(nome=nome, telefone=telefone, endereco=endereco)
    _cliente_repo.add(cliente)
    return cliente.id


def criar_restaurante(nome: str) -> str:
    restaurante = Restaurante(nome=nome)
    _restaurante_repo.add(restaurante)
    return restaurante.id


def criar_pedido(cliente: str, produtos: list[dict]) -> str:
    itens = [Produto(nome=p["nome"], preco=p["preco"]) for p in produtos]
    pedido = Pedido(cliente=cliente, itens=itens)
    _pedido_repo.add(pedido)
    _entregas[pedido.id] = Entrega(pedido_id=pedido.id)
    return pedido.id


def consultar_pedido(pedido_id: str) -> Pedido:
    pedido = _pedido_repo.get(pedido_id)
    if pedido is None:
        raise ValueError("pedido não encontrado")
    return pedido


def atualizar_status_entrega(pedido_id: str, novo_status: str) -> str:
    entrega = _entregas.get(pedido_id)
    if entrega is None:
        raise ValueError("entrega não encontrada")
    entrega.status = novo_status
    return entrega.status


def listar_pedidos_do_cliente(cliente: str) -> list[Pedido]:
    return [pedido for pedido in _pedido_repo.list() if pedido.cliente == cliente]