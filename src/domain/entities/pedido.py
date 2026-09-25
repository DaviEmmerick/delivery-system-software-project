from collections.abc import Iterable

from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.produto import Produto


class Pedido:
    def __init__(self, cliente: str, itens: Iterable[Produto | ItemPedido]):
        if not cliente or not cliente.strip():
            raise ValueError("cliente é obrigatório")
        if not itens:
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

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.itens)
