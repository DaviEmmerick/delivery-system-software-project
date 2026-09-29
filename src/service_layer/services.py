# Serviços do sistema de delivery.
from src.domain.entities.cliente import Cliente
from src.domain.entities.endereco import Endereco
from src.domain.entities.entrega import Entrega
from src.domain.entities.pedido import Pedido
from src.domain.entities.produto import Produto
from src.domain.entities.restaurante import Restaurante

_clientes: dict[str, Cliente] = {}
_restaurantes: dict[str, Restaurante] = {}
_pedidos: dict[str, Pedido] = {}
_entregas: dict[str, Entrega] = {}
_contador_pedidos = 0


def criar_cliente(nome: str, telefone: str, rua: str | None = None, numero: str | None = None) -> str:
    endereco = Endereco(rua=rua, numero=numero) if rua and numero else None
    cliente = Cliente(nome=nome, telefone=telefone, endereco=endereco)
    _clientes[cliente.nome] = cliente
    return cliente.nome


def criar_restaurante(nome: str) -> str:
    restaurante = Restaurante(nome=nome)
    _restaurantes[restaurante.nome] = restaurante
    return restaurante.nome


def criar_pedido(cliente: str, produtos: list[dict]) -> str:
    global _contador_pedidos
    itens = [Produto(nome=p["nome"], preco=p["preco"]) for p in produtos]
    pedido = Pedido(cliente=cliente, itens=itens)

    _contador_pedidos += 1
    pedido_id = str(_contador_pedidos)
    _pedidos[pedido_id] = pedido
    _entregas[pedido_id] = Entrega(pedido_id=pedido_id)
    return pedido_id


def consultar_pedido(pedido_id: str) -> Pedido:
    pedido = _pedidos.get(pedido_id)
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
    return [pedido for pedido in _pedidos.values() if pedido.cliente == cliente]
