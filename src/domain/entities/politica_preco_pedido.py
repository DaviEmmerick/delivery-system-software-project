import math
from dataclasses import dataclass
from typing import Protocol, Sequence

from src.domain.entities.item_pedido import ItemPedido


class PoliticaPrecoPedido(Protocol):
    def calcular(self, itens: Sequence[ItemPedido]) -> float:
        ...


class PrecoRegular:
    def calcular(self, itens: Sequence[ItemPedido]) -> float:
        return sum(item.subtotal for item in itens)


@dataclass(frozen=True)
class DescontoPercentual:
    percentual: float

    def __post_init__(self) -> None:
        if (
            isinstance(self.percentual, bool)
            or not isinstance(self.percentual, (int, float))
        ):
            raise ValueError("percentual de desconto deve estar entre 0 e 100")
        try:
            percentual_normalizado = float(self.percentual)
        except (OverflowError, ValueError):
            raise ValueError("percentual de desconto deve estar entre 0 e 100") from None
        if not math.isfinite(percentual_normalizado) or not 0 <= percentual_normalizado <= 100:
            raise ValueError("percentual de desconto deve estar entre 0 e 100")
        object.__setattr__(self, "percentual", percentual_normalizado)

    def calcular(self, itens: Sequence[ItemPedido]) -> float:
        total = sum(item.subtotal for item in itens)
        return total * (1 - self.percentual / 100)
