from dataclasses import dataclass

from src.domain.entities.produto import Produto


@dataclass(frozen=True)
class ItemPedido:
    produto: Produto
    quantidade: int = 1

    def __post_init__(self):
        if not isinstance(self.produto, Produto):
            raise ValueError("produto do item deve ser um Produto")
        if isinstance(self.quantidade, bool) or not isinstance(self.quantidade, int) or self.quantidade < 1:
            raise ValueError("quantidade deve ser um inteiro positivo")

    @property
    def subtotal(self) -> float:
        return self.produto.preco * self.quantidade