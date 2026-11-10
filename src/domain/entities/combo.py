from typing import Protocol, runtime_checkable

from src.domain.entities.produto import Produto


@runtime_checkable
class ComponenteItem(Protocol):
    """Component (GoF Composite): interface comum para itens simples e composições."""

    def nome(self) -> str:
        ...

    def preco(self) -> float:
        ...


class Item:
    """Leaf (GoF Composite): item individual/atômico sem filhos."""

    def __init__(self, nome: str, valor: float):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("nome do item é obrigatório")
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("valor do item não pode ser negativo")

        self._nome = nome.strip()
        self._valor = float(valor)

    def nome(self) -> str:
        return self._nome

    def preco(self) -> float:
        return self._valor

    def para_produto(self) -> Produto:
        return Produto(nome=self._nome, preco=self._valor)

    def __repr__(self) -> str:
        return f"Item(nome='{self._nome}', valor={self._valor})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return False
        return self._nome == other._nome and self._valor == other._valor


class Combo:
    """Composite (GoF Composite): agrupa itens simples ou outros combos aplicando desconto."""

    def __init__(self, nome: str, desconto: float = 0.0):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("nome do combo é obrigatório")
        if isinstance(desconto, bool) or not isinstance(desconto, (int, float)) or not (0.0 <= desconto <= 1.0):
            raise ValueError("desconto deve ser um valor decimal entre 0.0 e 1.0")

        self._nome = nome.strip()
        self._desconto = float(desconto)
        self._filhos: list[ComponenteItem] = []

    def adicionar(self, item: ComponenteItem) -> "Combo":
        if not isinstance(item, ComponenteItem):
            raise ValueError("apenas instâncias de ComponenteItem podem ser adicionadas ao combo")
        self._filhos.append(item)
        return self

    def remover(self, item: ComponenteItem) -> None:
        self._filhos.remove(item)

    @property
    def filhos(self) -> tuple[ComponenteItem, ...]:
        return tuple(self._filhos)

    @property
    def desconto(self) -> float:
        return self._desconto

    def nome(self) -> str:
        return self._nome

    def preco(self) -> float:
        total = sum(f.preco() for f in self._filhos)
        return total * (1.0 - self._desconto)

    def para_produto(self) -> Produto:
        return Produto(nome=self._nome, preco=round(self.preco(), 2))

    def __repr__(self) -> str:
        return f"Combo(nome='{self._nome}', desconto={self._desconto}, filhos={len(self._filhos)})"
