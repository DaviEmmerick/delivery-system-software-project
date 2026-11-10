from collections.abc import Iterable
from uuid import uuid4

from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.politica_preco_pedido import PoliticaPrecoPedido, PrecoRegular


class Pedido:
    def __init__(
        self,
        cliente: str,
        itens: Iterable[ItemPedido],
        id: str | None = None,
    ):
        if not isinstance(cliente, str) or not cliente.strip():
            raise ValueError("cliente é obrigatório")
        if itens is None:
            raise ValueError("pedido deve conter ao menos um item")
        if not isinstance(itens, Iterable):
            raise ValueError("pedido deve conter ao menos um item")

        itens_normalizados = tuple(itens)
        if any(not isinstance(item, ItemPedido) for item in itens_normalizados):
            raise ValueError("itens do pedido devem ser ItemPedido")
        self.cliente = cliente.strip()
        self.itens = itens_normalizados
        if not self.itens:
            raise ValueError("pedido deve conter ao menos um item")
        self.id = id or uuid4().hex

    @property
    def total(self) -> float:
        return self.calcular_total(PrecoRegular())

    def calcular_total(self, politica: PoliticaPrecoPedido) -> float:
        return politica.calcular(self.itens)
