from collections.abc import Iterable, Iterator
from typing import TypeAlias

from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.pedido import Pedido
from src.domain.entities.produto import Produto


ItemPedidoInput: TypeAlias = Produto | ItemPedido


class PedidoFactory:
    @staticmethod
    def criar(
        cliente: str,
        itens: Iterable[ItemPedidoInput] | None,
        id: str | None = None,
    ) -> Pedido:
        def normalizar_itens() -> Iterator[ItemPedido]:
            if itens is None or not isinstance(itens, Iterable):
                raise ValueError("pedido deve conter ao menos um item")
            for item in itens:
                if isinstance(item, Produto):
                    yield ItemPedido(item)
                elif isinstance(item, ItemPedido):
                    yield item
                else:
                    raise ValueError("itens do pedido devem ser Produtos ou ItemPedido")

        return Pedido(cliente=cliente, itens=normalizar_itens(), id=id)
