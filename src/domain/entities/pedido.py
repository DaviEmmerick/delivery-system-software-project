from collections.abc import Iterable
from uuid import uuid4

from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.produto import Produto


class Pedido:
    def __init__(
        self,
        cliente: str,
        itens: Iterable[Produto | ItemPedido],
        id: str | None = None,
    ):
        if not isinstance(cliente, str) or not cliente.strip():
            raise ValueError("cliente é obrigatório")
        if itens is None:
            raise ValueError("pedido deve conter ao menos um item")
        if not isinstance(itens, Iterable):
            raise ValueError("pedido deve conter ao menos um item")

        itens_normalizados = []
        for item in itens:
            if isinstance(item, Produto):
                itens_normalizados.append(ItemPedido(item))
            elif isinstance(item, ItemPedido):
                itens_normalizados.append(item)
            else:
                raise ValueError("itens do pedido devem ser Produtos ou ItemPedido")

        self.cliente = cliente.strip()
        self.itens = tuple(itens_normalizados)
        if not self.itens:
            raise ValueError("pedido deve conter ao menos um item")
        self.id = id or uuid4().hex

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.itens)
